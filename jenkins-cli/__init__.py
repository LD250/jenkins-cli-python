#!/usr/bin/python
#from jenkins import *

import argparse

parser = argparse.ArgumentParser(prog='jenkins')
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
print args
