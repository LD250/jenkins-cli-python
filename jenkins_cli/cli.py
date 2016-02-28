from __future__ import print_function
import os
import time
import datetime
import jenkins
import socket
from xml.etree import ElementTree

COLORS = {'blue': '\033[94m',
          'green': '\033[92m',
          'red': '\033[91m',
          'yellow': '\033[93m',
          'disabled': '\033[97m',
          'endcollor': '\033[0m',
          'aborted': '\033[97m(aborted)',
          'yellow_anime': '\033[93m(running)',
          'blue_anime': '\033[94m(running)',
          'red_anime': '\033[91m(running)'}


class CliException(Exception):
    pass


class JenkinsCli(object):
    SETTINGS_FILE_NAME = '.jenkins-cli'

    QUEUE_EMPTY_TEXT = "Building Queue is empty"

    def __init__(self, args, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.jenkins = self.auth(args.host, args.username, args.password, timeout)

    @classmethod
    def auth(cls, host=None, username=None, password=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        if host is None or username is None or password is None:
            settings_dict = cls.read_settings_from_file()
            try:
                host = host or settings_dict['host']
                username = username or settings_dict.get('username', None)
                password = password or settings_dict.get('password', None)
            except KeyError:
                raise CliException('jenkins "host" has to be specified by the command-line options or in .jenkins-cli file')
        return jenkins.Jenkins(host, username, password, timeout)

    @classmethod
    def read_settings_from_file(cls):
        try:
            current_folder = os.getcwd()
            filename = os.path.join(current_folder, cls.SETTINGS_FILE_NAME)
            if not os.path.exists(filename):
                home_folder = os.path.expanduser("~")
                filename = os.path.join(home_folder, cls.SETTINGS_FILE_NAME)
                if not os.path.exists(filename):
                    return {}
            f = open(filename, 'r')
            jenkins_settings = f.read()
        except Exception as e:
            raise CliException('Error reading %s: %s' % (filename, e))

        settings_dict = {}
        for setting_line in jenkins_settings.split('\n'):
            if "=" in setting_line:
                key, value = setting_line.split("=", 1)
                settings_dict[key.strip()] = value.strip()
        return settings_dict

    def run_command(self, args):
        command = args.jenkins_command
        getattr(self, command)(args)

    def jobs(self, args):
        jobs = self._get_jobs(args)
        for job in jobs:
            print("%s***%s %s" % (COLORS.get(job['color'], job['color']), COLORS['endcollor'], job['name']))

    def _get_jobs(self, args):
        jobs = self.jenkins.get_jobs()
        if args.a:
            jobs = [j for j in jobs if j.get('color') != 'disabled']
        # jobs = sorted(jobs, key=lambda j: j.get('name'))
        return jobs

    def queue(self, args):
        jobs = self.jenkins.get_queue_info()
        if jobs:
            for job in jobs:
                print("%s %s" % (job['task']['name'], job['why']))
        else:
            print(self.QUEUE_EMPTY_TEXT)

    def _check_job(self, job_name):
        job_name = self.jenkins.get_job_name(job_name)
        if not job_name:
            raise CliException('Job name does not esist')
        return job_name

    def info(self, args):
        job_name = self._check_job(args.job_name)
        job_info = self.jenkins.get_job_info(job_name, 1)
        if not job_info:
            job_info = {}
        last_build = job_info.get('lastBuild', {})
        last_success_build = job_info.get('lastSuccessfulBuild', {})
        info = ("Last build name: %s (result: %s)\n"
                "Last success build name: %s\n"
                "Build started: %s\n"
                "Building now: %s\n"
                "Mercurial branch set: %s")
        xml = self.jenkins.get_job_config(job_name)
        root = ElementTree.fromstring(xml.encode('utf-8'))
        rev = 'Not Known'
        scm = root.find('scm')
        if scm is not None:
            revision = scm.find('revision')
            if revision is not None:
                rev = revision.text
        print(info % (last_build.get('fullDisplayName', 'Not Built'),
                      last_build.get('result', 'Not Built'),
                      last_success_build.get('fullDisplayName', 'Not Built'),
                      datetime.datetime.fromtimestamp(last_build['timestamp'] / 1000) if last_build else 'Not built',
                      'Yes' if last_build.get('building') else 'No',
                      rev))

    def set_branch(self, args):
        job_name = self._check_job(args.job_name)
        xml = self.jenkins.get_job_config(job_name)
        root = ElementTree.fromstring(xml.encode('utf-8'))
        scm = root.find('scm')
        new_xml = None
        if scm is not None:
            revision = scm.find('revision')
            if revision is not None:
                revision.text = args.branch_name
                new_xml = ElementTree.tostring(root)
                self.jenkins.reconfig_job(job_name, new_xml)
                print('Done')
        if new_xml is None:
            print("Can not set revision info")

    def start(self, args):
        for job in args.job_name:
            job_name = self._check_job(job)
            start_status = self.jenkins.build_job(job_name)
            print("%s: %s" % (job_name, 'started' if not start_status else start_status))

    def stop(self, args):
        job_name = self._check_job(args.job_name)
        info = self.jenkins.get_job_info(job_name)
        build_number = info['lastBuild'].get('number')
        stop_status = self.jenkins.stop_build(job_name, build_number)
        print("%s: %s" % (job_name, 'stoped' if not stop_status else stop_status))

    def console(self, args):
        job_name = self._check_job(args.job_name)
        info = self.jenkins.get_job_info(job_name)
        print(info['lastBuild'])
        build_number = info['lastBuild'].get('number')
        console_out = self.jenkins.get_build_console_output(job_name, build_number)
        console_out = console_out.split('\n')
        last_line_num = len(console_out)
        if args.n:
            console_out = console_out[args.n:] if args.n < 0 else console_out[:args.n]
        print("\n".join(console_out))
        if args.i:
            build_info = self.jenkins.get_build_info(job_name, build_number)
            while build_info['building']:
                console_out = self.jenkins.get_build_console_output(job_name, build_number)
                console_out = console_out.split('\n')
                new_line_num = len(console_out)
                if new_line_num > last_line_num:
                    print("\n".join(console_out[last_line_num:]))
                    last_line_num = new_line_num
                time.sleep(3)
                build_info = self.jenkins.get_build_info(job_name, build_number)

    def building(self, args):
        args.a = True
        jobs = [j for j in self._get_jobs(args) if 'anime' in j['color']]
        if jobs:
            for job in jobs:
                info = self.jenkins.get_job_info(job['name'])
                build_number = info['lastBuild'].get('number')
                if build_number:
                    build_info = self.jenkins.get_build_info(job['name'], build_number)
                    eta = (build_info['timestamp'] + build_info['estimatedDuration']) / 1000 - time.time()
                    print("%s estimated time left %s" % (build_info['fullDisplayName'],
                                                         datetime.timedelta(seconds=eta)))
        else:
            print("Nothing is building now")
