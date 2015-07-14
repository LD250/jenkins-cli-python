usage: jenkins

Server URL, Username and password must be specified either by the command line
arguments or in configuration file (.jenkins). Command line arguments has the
highest priority, after that the .jenkins file from current folder is taking
into account. The lowest priority is for .jenkins file in program folder

optional arguments:
  -h, --help            show this help message and exit
  --jenkins-server url  Jenkins Server Url (http://jenkins/)
  --jenkins-username username
                        Jenkins Username
  --jenkins-password password
                        Jenkins Password

Available commands:
  {jobs,pending,start,stop,history}
    jobs                Show all jobs and their status
    pending             Shows pending jobs
    start               Start job
    stop                Stop job
    history             Show job history
