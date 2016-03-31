from __future__ import print_function

import argparse
from jenkins import JenkinsException

from jenkins_cli.cli import JenkinsCli, CliException, get_jobs_legend
from jenkins_cli.version import version


def main():
    parser = argparse.ArgumentParser(prog='jenkins',
                                     description='Host, username and password may be specified either by the command line arguments '
                                                 'or in the configuration file (.jenkins-cli). Command line arguments have the highest priority, '
                                                 'after that the .jenkins-cli file from current folder is used. If there is no'
                                                 '.jenkins-cli file in the current folder, settings will be read from .jenkins-cli located in the home'
                                                 'folder')
    parser.add_argument('--host', metavar='jenkins-url', help='Jenkins Host', default=None)
    parser.add_argument('--username', metavar='username', help='Jenkins Username', default=None)
    parser.add_argument('--password', metavar='password', help='Jenkins Password', default=None)
    parser.add_argument('--version', '-v', action='version', version='jenkins-cli %s' % version)

    subparsers = parser.add_subparsers(title='Available commands', dest='jenkins_command')

    jobs_parser = subparsers.add_parser('jobs',
                                        help='Show all jobs and their statuses',
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        description="Status description:\n\n" + "\n".join(get_jobs_legend()))
    jobs_parser.add_argument('-a', help='show only active jobs', default=False, action='store_true')
    jobs_parser.add_argument('-p', help='show only jobs in build progress', default=False, action='store_true')

    subparsers.add_parser('queue', help='Show builds queue')

    subparsers.add_parser('building', help='Build executor status')

    builds_parser = subparsers.add_parser('builds', help='Show builds for the job')
    builds_parser.add_argument('job_name', help='Job name of the builds')

    start_parser = subparsers.add_parser('start', help='Start job')
    start_parser.add_argument('job_name', help='Job to start', nargs='*')

    start_parser = subparsers.add_parser('info', help='Job info')
    start_parser.add_argument('job_name', help='Job to get info for')

    set_branch = subparsers.add_parser('setbranch', help='Set VCS branch (Mercurial or Git)')
    set_branch.add_argument('job_name', help='Job to set branch for')
    set_branch.add_argument('branch_name', help='Name of the VCS branch')

    stop_parser = subparsers.add_parser('stop', help='Stop job')
    stop_parser.add_argument('job_name', help='Job to stop')

    console_parser = subparsers.add_parser('console', help='Show console for the build')
    console_parser.add_argument('job_name', help='Job to show console for')
    console_parser.add_argument('-b', '--build', help='job build number to show console for (if omitted, last build number is used)', default='')
    console_parser.add_argument('-n', help='show first n lines only(if n is negative, show last n lines)', type=int)
    console_parser.add_argument('-i', help='interactive console', default=False, action='store_true')

    console_parser = subparsers.add_parser('changes', help="Show build's changes")
    console_parser.add_argument('job_name', help='Job to show changes for')
    console_parser.add_argument('-b', '--build', help='job build number to show changes for (if omitted, last build number is used)', default='')

    args = parser.parse_args()
    try:
        if args.jenkins_command is None:
            parser.print_help()
        else:
            JenkinsCli(args).run_command(args)
    except JenkinsException as e:
        print("Jenkins server response: %s:" % e)
    except KeyboardInterrupt:
        print("Aborted")
    except CliException as e:
        print(e)
        print("Read jenkins --help")


if __name__ == "__main__":
    main()
