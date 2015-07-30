import os
import jenkins

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


def read_settings_from_file():
    try:
        current_folder = os.getcwd()
        filename = current_folder + "/.jenkins-cli"
        if not os.path.exists(filename):
            program_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = program_folder + "/.jenkins-cli"
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


def auth(host=None, username=None, password=None):
    if host is None or username is None or password is None:
        settings_dict = read_settings_from_file()
        try:
            host = host or settings_dict['host']
            username = username or settings_dict['username']
            password = password or settings_dict['password']
        except KeyError:
            raise CliException('host, username and password has to be specified by the command-line options or .jenkins-cli file')
    j = jenkins.Jenkins(host, username, password)
    return j


def get_queue_jobs(args):
    jenkins = auth(args.host, args.username, args.password)
    jobs = jenkins.get_queue_info()
    if jobs:
        for job in jobs:
            print "%s %s" % (job['task']['name'], job['why'])
    else:
        print "Building Queue is empty"


def get_building_jobs(args):
    pass


def get_jobs(args):
    jenkins = auth(args.host, args.username, args.password)
    jobs = jenkins.get_jobs()
    if not args.d:
        jobs = [j for j in jobs if j.get('color') != 'disabled']
    jobs = sorted(jobs, key=lambda j: j.get('name'))
    for job in jobs:
        print "%s***%s %s" % (colors.get(job['color'], job['color']), colors['endcollor'], job['name'])

