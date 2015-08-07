##!/usr/bin/env python
import argparse
import jenkins_cli


def main():
    parser = argparse.ArgumentParser(prog='jenkins',
                                     #usage='%(prog)s',
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

    q_parser = subparsers.add_parser('queue', help='Shows builds queue')

    b_parser = subparsers.add_parser('building', help='Build executor status')

    start_parser = subparsers.add_parser('start', help='Start job')
    start_parser.add_argument('job_name', help='Job to start', nargs='*')
    #start_parser.add_argument('-s', help='Silent mode (return only build number)')

    start_parser = subparsers.add_parser('info', help='Job info')
    start_parser.add_argument('job_name', help='Job to to get info for')

    stop_parser = subparsers.add_parser('stop', help='Stop job')
    stop_parser.add_argument('job_name', help='Job to stop')

    console_parser = subparsers.add_parser('console', help='Show job history')
    console_parser.add_argument('job_name', help='Job to show history for')
    console_parser.add_argument('-n', help='Show num of the lines from the end only', type=int)

    args = parser.parse_args()
    try:
        jenkins_cli.JenkinsCli(args).run_command(args)
    except jenkins_cli.jenkins.JenkinsException as e:
        print e
    except jenkins_cli.CliException as e:
        print e
        print "Read jenkins --help"
#    except Exception as e:
#        raise e 


if __name__ == "__main__":
    main()

