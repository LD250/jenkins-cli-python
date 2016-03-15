# Jenkins command line interface
[![PyPI version](https://badge.fury.io/py/jenkins-cli.svg)](https://badge.fury.io/py/jenkins-cli)
[![Build Status](https://travis-ci.org/LD250/jenkins-cli-python.svg?branch=master)](https://travis-ci.org/LD250/jenkins-cli-python)
[![Code Health](https://landscape.io/github/LD250/jenkins-cli-python/master/landscape.svg?style=flat)](https://landscape.io/github/LD250/jenkins-cli-python/master)
[![Requirements Status](https://requires.io/github/LD250/jenkins-cli-python/requirements.svg?branch=master)](https://requires.io/github/LD250/jenkins-cli-python/requirements/?branch=master)

# Install:
```bash
git clone https://github.com/LD250/jenkins-cli-python.git
cd jenkins-cli-python
python setup.py install
```

# Usage:

```bash
jenkins [-h] [--host jenkins-url] [--username username]
         [--password password]
         {jobs,queue,building,start,info,set_branch,stop,console} ...
```

Server URL, Username and password may be specified either by the command line arguments or in configuration file **(.jenkins-cli)**. Command line arguments has the highest priority, after that the **.jenkins-cli** file from current folder is taking into account. If there is no.jenkins-cli file in current folder, settings will be read from **.jenkins-cli** from the home folder

# Optional arguments:
```bash
  -h, --help            show this help message and exit
  --host jenkins-url    Jenkins Server Url
  --username username   Jenkins Username
  --password password   Jenkins Password
```

# Available commands:
```bash
  {jobs,queue,building,start,info,set_branch,stop,console}
    jobs                Show all jobs and their statuses
    queue               Shows builds queue
    building            Build executor status
    start               Start job
    info                Job info
    set_branch          Set SCM branch
    stop                Stop job
    console             Show console for last build
```
