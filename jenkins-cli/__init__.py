##!/usr/bin/env python
import argparse
import jenkins_cli


def main():
    parser = argparse.ArgumentParser(prog='jenkins',
                                     #usage='%(prog)s',
                                     description='Server URL, Username and password may be specified either by the command line arguments '
                                                 'or in configuration file (.jenkins-cli). Command line arguments has the highest priority, '
                                                 'after that the .jenkins-cli file from current folder is taking into account.')
    parser.add_argument('--host', metavar='jenkins-url', help='Jenkins Server Url', default=None)
    parser.add_argument('--username', metavar='username', help='Jenkins Username', default=None)
    parser.add_argument('--password', metavar='password', help='Jenkins Password', default=None)

    subparsers = parser.add_subparsers(title='Available commands')

    jobs_parser = subparsers.add_parser('jobs', help='Show all jobs and their status')
    jobs_parser.set_defaults(func=jenkins_cli.get_jobs)
    jobs_parser.add_argument('-d', help='Show disabled jobs', default=False, action='store_true')

    q_parser = subparsers.add_parser('pending', help='Shows pending jobs')

    start_parser = subparsers.add_parser('start', help='Start job')
    start_parser.add_argument('job_name', help='Job to start')
    start_parser.add_argument('-s', help='Silent mode (return only build number)')

    stop_parser = subparsers.add_parser('stop', help='Stop job')
    stop_parser.add_argument('job_name', help='Job to stop')

    history_parser = subparsers.add_parser('history', help='Show job history')
    history_parser.add_argument('job_name', help='Job to show history for')
    history_parser.add_argument('-n', help='Show num of records only')

    args = parser.parse_args()
    try:
        args.func(args)
    except jenkins_cli.CliException as e:
        print e
        print "Read jenkins --help"
#    except Exception as e:
#        raise e 


if __name__ == "__main__":
    main()

