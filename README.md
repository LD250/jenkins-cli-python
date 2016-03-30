# Jenkins command line interface
[![PyPI version](https://badge.fury.io/py/jenkins-cli.svg)](https://badge.fury.io/py/jenkins-cli)
[![Build Status](https://travis-ci.org/LD250/jenkins-cli-python.svg?branch=master)](https://travis-ci.org/LD250/jenkins-cli-python)
[![Code Health](https://landscape.io/github/LD250/jenkins-cli-python/master/landscape.svg?style=flat)](https://landscape.io/github/LD250/jenkins-cli-python/master)
[![Requirements Status](https://requires.io/github/LD250/jenkins-cli-python/requirements.svg?branch=master)](https://requires.io/github/LD250/jenkins-cli-python/requirements/?branch=master)

**Based on**
[python-jenkins](https://github.com/openstack/python-jenkins)

# Tested on
Jenkins ver: 1.565, 
Python ver: 2.7, 3.4, 3.5

# Table of contents
 * [Installation](#installation)
 * [Commands overwiew](#commands-overwiew)
 * [Usage example](#usage-example)
 * [Tests](#tests)

# Installation:

## Using pip

## Clone 
```bash
git clone https://github.com/LD250/jenkins-cli-python.git
cd jenkins-cli-python
python setup.py install
```

## Configuration file (.jencins-cli)

Server URL, Username and password may be specified either by the command line arguments or in configuration file **(.jenkins-cli)**. Command line arguments has the highest priority, after that the **.jenkins-cli** file from current folder is taking into account. If there is no.jenkins-cli file in current folder, settings will be read from **.jenkins-cli** from the home folder

# Commands overwiew:
```bash
  {jobs,queue,building,start,info,set_branch,stop,console}
    jobs                Show all jobs and their statuses
    queue               Shows builds queue
    building            Build executor status
    start               Start job
    info                Job info
    setbranch           Set SCM branch
    stop                Stop job
    console             Show console for the build
    builds             	Show builds for job
    changes            	Show build's changes
```

# Usage example:

```bash
jenkins [-h] [--host jenkins-url] [--username username] [--password password]
         {jobs,queue,building,start,info,setbranch,stop,console} ...
```

# Tests

To perfom flake8 checks and run tests similar to Travis

```bash
pip install -r requirements.txt
tox 
```


