from __future__ import print_function

from jenkins import JenkinsException

from jenkins_cli.cli import JenkinsCli, CliException
from jenkins_cli.cli_arguments import load_parser


def main():
    parser = load_parser()
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
