# Jenkins command line interface
[![PyPI version](https://badge.fury.io/py/jenkins-cli.svg)](https://badge.fury.io/py/jenkins-cli)
[![Build Status](https://travis-ci.org/LD250/jenkins-cli-python.svg?branch=master)](https://travis-ci.org/LD250/jenkins-cli-python)
[![Code Health](https://landscape.io/github/LD250/jenkins-cli-python/master/landscape.svg?style=flat)](https://landscape.io/github/LD250/jenkins-cli-python/master)
[![Requirements Status](https://requires.io/github/LD250/jenkins-cli-python/requirements.svg?branch=master)](https://requires.io/github/LD250/jenkins-cli-python/requirements/?branch=master)

**Based on**
[python-jenkins](https://github.com/openstack/python-jenkins)

# Tested on
Jenkins ver: 1.565, 1.655

Python ver: 2.7, 3.4, 3.5

# Table of contents
 * [Installation](#installation)
 * [Commands overview](#commands-overview)
 * [Usage example](#usage-example)
 * [Tests](#tests)

# Installation:

```bash
pip isntall jenkins-cli
```

or
 
```bash
git clone https://github.com/LD250/jenkins-cli-python.git
cd jenkins-cli-python
python setup.py install
```

## Configuration file (.jenkins-cli)

Host, username and password may be specified either by the command line arguments or in the configuration file **(.jenkins-cli)**. Command line arguments have the highest priority, after that the **.jenkins-cli** file from current folder is used. If there is no.jenkins-cli file in the current folder, settings will be read from **.jenkins-cli** located in the home folder

**.jenkins-cli** example
```txt
host=http://localhost:8082/
username=username
password=******
```

# Commands overview:
    jobs                Show all jobs and their statuses
    queue               Show builds queue
    building            Build executor status
    start               Start job
    info                Job info
    setbranch           Set VCS branch (Mercurial or Git)
    stop                Stop job
    console             Show console for the build
    builds             	Show builds for the job
    changes            	Show build's changes
Run `jenkins --help` for detailed help. To view optional parameters, run `--help` for the specific command. For example `jenkins jobs --help` will show job status description and optional arguments.


# Usage example:

Show status descriptions
```bash
$ jenkins jobs --help
usage: jenkins jobs [-h] [-a] [-p]

Status description:

... -> Unknown
F.. -> Failed
D.. -> Disabled
U.. -> Unstable
N.. -> Not built
S.. -> Stable
A.. -> Aborted
.>> -> Build in progress

optional arguments:
  -h, --help  show this help message and exit
  -a          show only active jobs
  -p          show only jobs in build progress
```
Show jobs
```bash
$ jenkins jobs
D.. hudson
S.. jenkins-cli
U>> new-project
```
Show job info
```bash
$ jenkins info jenkins-cli
Last build name: jenkins-cli #18 (result: SUCCESS)
Last success build name: jenkins-cli #18
Build started: 2016-03-31 00:22:38.326999
Building now: No
Git branch set to: master
```
Update VCS branch
```bash
$ jenkins setbranch new-feature
Done
```
Run job
```bash
$ jenkins start jenkins-cli
jenkins-cli: started
```
View job builds
```bash
$ jenkins builds jenkins-cli
S.. #18 0:00:07 (2 commits)
S.. #17 0:00:08 (2 commits)
F.. #16 0:00:00 (4 commits)
S.. #15 0:00:08 (2 commits)
```
Show previous build changes
```bash
$ jenkins changes jenkins-cli -b 17
1. add .travis.yml from add-travis branch by Denys Levchenko affected 1 files 
2. scaffolding for tests by Denys Levchenko affected 5 files 
```
Show current job console output (last 13 lines)
```bash
$ jenkins console jenkins-cli -n 13
test_jobs (tests.test_cli.TestCliCommands) ... ok
test_queue (tests.test_cli.TestCliCommands) ... ok
test_set_branch (tests.test_cli.TestCliCommands) ... ok
test_start (tests.test_cli.TestCliCommands) ... ok
test_stop (tests.test_cli.TestCliCommands) ... ok
test_read_settings_from_file (tests.test_cli.TestCliFileUsing) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.015s

OK
Finished: SUCCESS
```

# Tests

To perform flake8 checks and run tests similar to Travis, do the following

```bash
pip install -r requirements.txt
tox 
```


