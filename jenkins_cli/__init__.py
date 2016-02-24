import argparse
from jenkins import JenkinsException

from jenkins_cli.cli import JenkinsCli, CliException


def main():
    parser = argparse.ArgumentParser(prog='jenkins',
                                     description='Server URL, Username and password may be specified either by the command line arguments '
                                                 'or in configuration file (.jenkins-cli). Command line arguments has the highest priority, '
                                                 'after that the .jenkins-cli file from current folder is taking into account. If there is no'
                                                 '.jenkins-cli file in current folder, setiings will be read from .jenkins-cli from the program'
                                                 'folder')
    parser.add_argument('--host', metavar='jenkins-url', help='Jenkins Server Url', default=None)
    parser.add_argument('--username', metavar='username', help='Jenkins Username', default=None)
    parser.add_argument('--password', metavar='password', help='Jenkins Password', default=None)

    subparsers = parser.add_subparsers(title='Available commands', dest='jenkins_command')

    jobs_parser = subparsers.add_parser('jobs', help='Show all jobs and their status')
    jobs_parser.add_argument('-d', help='Show disabled jobs', default=False, action='store_true')

    subparsers.add_parser('queue', help='Shows builds queue')

    subparsers.add_parser('building', help='Build executor status')

    start_parser = subparsers.add_parser('start', help='Start job')
    start_parser.add_argument('job_name', help='Job to start', nargs='*')

    start_parser = subparsers.add_parser('info', help='Job info')
    start_parser.add_argument('job_name', help='Job to to get info for')

    set_branch = subparsers.add_parser('set_branch', help='Job info')
    set_branch.add_argument('job_name', help='Job to to set branch')
    set_branch.add_argument('branch_name', help='Name of the branch')

    stop_parser = subparsers.add_parser('stop', help='Stop job')
    stop_parser.add_argument('job_name', help='Job to stop')

    console_parser = subparsers.add_parser('console', help='Show job history')
    console_parser.add_argument('job_name', help='Job to show history for')
    console_parser.add_argument('-n', help='Show first n num of the lines only(if n is negative, shows last n lines)', type=int)
    console_parser.add_argument('-i', help='Interactive console', default=False, action='store_true')

    args = parser.parse_args()
    try:
        JenkinsCli(args).run_command(args)
    except JenkinsException as e:
        print(e)
    except KeyboardInterrupt:
        print("Aborted")
    except CliException as e:
        print(e)
        print("Read jenkins --help")


if __name__ == "__main__":
    main()
