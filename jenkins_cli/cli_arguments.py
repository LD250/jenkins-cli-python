import argparse

from jenkins_cli.cli import get_jobs_legend
from jenkins_cli.version import version


def load_parser():
    """
    Create a parser and load it with CLI arguments

    Returns: ArgumentParser instance
    """
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
    parser.add_argument('-e', '--environment',
                        help='Which config section to use')

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

    start_parser = subparsers.add_parser('configxml', help='Job config in xml format')
    start_parser.add_argument('job_name', help='Job to get config for')

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
    console_parser.add_argument('-t', '--interval', help='refresh interval in seconds (in case of interactive console -i)', default=3, type=check_nonnegative)

    changes_parser = subparsers.add_parser('changes', help="Show build's changes")
    changes_parser.add_argument('job_name', help='Job to show changes for')
    changes_parser.add_argument('-b', '--build', help='job build number to show changes for (if omitted, last build number is used)', default='')

    return parser


def check_nonnegative(value):
    """
    Checks if (possibly string) value is non-negative integer and returns it.

    Raise:
        ArgumentTypeError: if value is not a non-negative integer
    """
    try:
        ivalue = int(value)
        if ivalue < 0:
            raise ValueError()
    except:
        raise argparse.ArgumentTypeError("Value must be a non-negative integer: %s" % value)
    return ivalue
