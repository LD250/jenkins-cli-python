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

    subparsers = parser.add_subparsers(title='Available commands')

    jobs_parser = subparsers.add_parser('jobs', help='Show all jobs and their status')
    jobs_parser.add_argument('-d', help='Show disabled jobs', default=False, action='store_true')
    jobs_parser.set_defaults(func=jenkins_cli.get_jobs)

    q_parser = subparsers.add_parser('queue', help='Shows builds queue')
    q_parser.set_defaults(func=jenkins_cli.get_queue_jobs)

    b_parser = subparsers.add_parser('building', help='Build executor status')
    b_parser.set_defaults(func=jenkins_cli.get_building_jobs)

    start_parser = subparsers.add_parser('start', help='Start job')
    start_parser.add_argument('job_name', help='Job to start')
    start_parser.add_argument('-s', help='Silent mode (return only build number)')
    start_parser.set_defaults(func=jenkins_cli.start_job)

    stop_parser = subparsers.add_parser('stop', help='Stop job')
    stop_parser.add_argument('job_name', help='Job to stop')
    stop_parser.set_defaults(func=jenkins_cli.stop_job)

    console_parser = subparsers.add_parser('console', help='Show job history')
    console_parser.add_argument('job_name', help='Job to show history for')
    console_parser.add_argument('-n', help='Show num of the lines from the end only', type=int)
    console_parser.set_defaults(func=jenkins_cli.show_console_output)

    args = parser.parse_args()
    try:
        args.func(args)
    except jenkins_cli.jenkins.JenkinsException as e:
        print e
    except jenkins_cli.CliException as e:
        print e
        print "Read jenkins --help"
#    except Exception as e:
#        raise e 


if __name__ == "__main__":
    main()

