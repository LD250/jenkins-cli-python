#!/usr/bin/python
#from jenkins import *
import os
import argparse


def main():
    parser = argparse.ArgumentParser(prog='jenkins',
                                     usage='%(prog)s',
                                     description='Server URL, Username and password must be specified either by the command line arguments '
                                                 'or in configuration file (.jenkins). Command line arguments has the highest priority, '
                                                 'after that the .jenkins file from current folder is taking into account. The lowest priority '
                                                 'is for .jenkins file in program folder')
    parser.add_argument('--jenkins-server', metavar='url', help='Jenkins Server Url (http://jenkins/)')
    parser.add_argument('--jenkins-username', metavar='username', help='Jenkins Username')
    parser.add_argument('--jenkins-password', metavar='password', help='Jenkins Password')

    subparsers = parser.add_subparsers(title='Available commands')

    jobs_parser = subparsers.add_parser('jobs', help='Show all jobs and their status')

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

    program_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_folder = os.getcwd()
    print args

main()

