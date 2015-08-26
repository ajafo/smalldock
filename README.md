# smalldock
Small docker manager

#Description
This is simple small docker images manager. You can run many instances with outgoing transfer via external IP and generate upstreams for nginx.

#Dependencies
You need python-docker:

pip install python-docker


#How it works
Just run smalldock.py script. It read configuration and check working machines. After this start reading docker events stream.
When you start new docker container smalldock remember it IP, and generate upstream file for nginx.
Moreover if container have assigned external IP in config file it create iptables rule for outgoing transfer.
When container die it remove IP from upstream and delete iptables rule.

#Configuration
```ini
[ubuntu]
image: ubuntu:trusty
ext_ip: 10.119.58.155,10.119.58.156
port: 0
version: trusty
onstart: 2
```

[ubuntu] - image name
version - image version
ext_ip - comma separated list of external IP's, if you don't want to assign external ip set this value on 0 e.g. ext_ip: 0
port - not used yet
version - image version
onstart - how many containers of this type should be working on smalldock start, e.g. if you set onstart: 5, and when smalldock starts will work only 2 machines of this type, then it start another 3 machines


