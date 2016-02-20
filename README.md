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

Server URL, Username and password may be specified either by the command line arguments or in configuration file **(.jenkins-cli)**. Command line arguments has the highest priority, after that the **.jenkins-cli** file from current folder is taking into account. If there is no.jenkins-cli file in current folder, settings will be read from **.jenkins-cli** from the program folder

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
    jobs                Show all jobs and their status
    queue               Shows builds queue
    building            Build executor status
    start               Start job
    info                Job info
    set_branch          Job info
    stop                Stop job
    console             Show job history
```
