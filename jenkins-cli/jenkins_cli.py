import os
import time
import datetime
import jenkins
import socket

colors = {'blue': '\033[94m',
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


class JenkinsCli(jenkins.Jenkins):
    SETTINGS_FILE_NAME = '.jenkins-cli'

    def __init__(self, args, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        url, username, password = self.auth(args.host, args.username, args.password)
        super(JenkinsCli, self).__init__(url, username, password, timeout=timeout)

    def auth(self, host=None, username=None, password=None):
        if host is None or username is None or password is None:
            settings_dict = self.read_settings_from_file()
            try:
                host = host or settings_dict['host']
                username = username or settings_dict['username'] or None
                password = password or settings_dict['password'] or None
            except KeyError:
                raise CliException('host, username and password has to be specified by the command-line options or .jenkins-cli file')
        return (host, username, password)

    def read_settings_from_file(self):
        try:
            current_folder = os.getcwd()
            filename = "%s/%s" % (current_folder, self.SETTINGS_FILE_NAME)
            if not os.path.exists(filename):
                program_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                filename = "%s/%s" % (program_folder, self.SETTINGS_FILE_NAME)
            f = open(filename, 'r')
            jenkins_settings = f.read()
        except Exception as e:
            raise CliException('Error reading %s: %s' % (filename, e))

        settings_dict = {}
        for setting_line in jenkins_settings.split('\n'):
            if "=" in setting_line:
                key, value = setting_line.split("=", 1)
                settings_dict[key] = value
        return settings_dict

    def run_command(self, args):
        command = args.jenkins_command
        getattr(self, command)(args)

    def jobs(self, args):
        jobs = self.get_jobs()
        for job in jobs:
            print "%s***%s %s" % (colors.get(job['color'], job['color']), colors['endcollor'], job['name'])

    def _get_jobs(self, args):
        jobs = self.get_jobs()
        if not args.d:
            jobs = [j for j in jobs if j.get('color') != 'disabled']
        jobs = sorted(jobs, key=lambda j: j.get('name'))
        return jobs

    def queue(self, args):
        jobs = self.get_queue_info()
        if jobs:
            for job in jobs:
                print "%s %s" % (job['task']['name'], job['why'])
        else:
            print "Building Queue is empty"

    def _check_job(self, job_name):
        job_name = self.get_job_name(job_name)
        if not job_name:
            raise CliException('Job name does not esist')
        return job_name

    def start(self, args):
        job_name = self._check_job(args.job_name)
        start_status = self.build_job(job_name)
        print "%s: %s" % (job_name, 'started' if not start_status else start_status)

    def stop(self, args):
        job_name = self._check_job(args.job_name)
        info = self.get_job_info(job_name)
        build_number = info['lastBuild'].get('number')
        stop_status = self.stop_build(job_name, build_number)
        print "%s: %s" % (job_name, 'stoped' if not stop_status else stop_status)

    def console(self, args):
        job_name = self._check_job(args.job_name)
        info = self.get_job_info(job_name)
        build_number = info['lastBuild'].get('number')
        console_out = self.get_build_console_output(job_name, build_number)
        if args.n:
            console_out = "\n".join(console_out.split('\n')[-args.n:])
        print console_out

    def building(self, args):
        args.d = False
        jobs = [j for j in self._get_jobs(args) if 'anime' in j['color']]
        if jobs:
            for job in jobs:
                info = self.get_job_info(job['name'])
                build_number = info['lastBuild'].get('number')
                if build_number:
                    build_info = self.get_build_info(job['name'], build_number)
                    eta = (build_info['timestamp'] + build_info['estimatedDuration']) / 1000 - time.time()
                    print "%s estimated time left %s" % (build_info['fullDisplayName'],
                                                         datetime.timedelta(seconds=eta))
        else:
            print "Nothing is building now"

