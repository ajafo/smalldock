#!/usr/bin/python

import os
import json
import docker
import executor
import threading
from configurator import ConfigFactory


dock = docker.Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)
print "number of containers = ", len(dock.containers(all))
print "docker version is python ", docker.version

conf = ConfigFactory()
conf.show_config_all()



def getSystemContainters():
        sc=dock.containers()
        for l in sc:
            instli=l["Image"].split(':')
            inst_name=instli[0]
            inst_ver=instli[1]
            id=l["Id"]
            startInstance(inst_name,id,inst_ver)



def print_config():
     print conf
     print dock.containers()


def startInstance(inst,id,inst_ver):
     print inst
     cnf=dock.inspect_container(id)
     ip_wew=cnf['NetworkSettings']['IPAddress']
     conf.li[inst].showIntIp()
     conf.li[inst].addIntIp(id,ip_wew)

     if conf.li[inst].ip_pool[0] is not "0":
         ip_zew=conf.li[inst].getFreeIp()
         print 'Assign external IP: ' + ip_zew
         executor.addIpRule(ip_wew,ip_zew)
         conf.li[inst].addExtIp(id,ip_zew)
     else:
         print "This machine have no IP assigned"


def stopInstance(inst,id,version):
     ip_wew=conf.li[inst].getIntIP(id)
     print ip_wew
     conf.li[inst].removeIntIp(id)
     if conf.li[inst].ip_pool[0] is not "0":
         ip_zew=conf.li[inst].getExtIp(id)
         print 'Deassign external IP: ' + ip_zew
         executor.delIpRule(ip_wew,ip_zew)
         conf.li[inst].removeExtIp(id)
     else:
         print "This machine have no IP to remove "










def runInstances(inst,ver,count):
    print 'Start instance ' + inst + ":" + ver, count
    for c in range(0,int(count)):
        container = dock.create_container(image=inst + ":" + ver)
        response = dock.start(container=container.get('Id'))
        print response








for (c,d) in conf.li.items():
   thread = threading.Thread(target=runInstances, args=(c,'latest',d.toStartInst()))
   thread.daemon = True
   thread.start()


getSystemContainters()



for (inst_name,d) in conf.li.items():
    upstream_file=conf.li[inst_name].getUpFile()
    conf.generate_upstrean(inst_name,d.showIntIp(),'latest',upstream_file)

executor.nginxRestart()




for line in dock.events():
     d=json.loads(line)

     instli=d["from"].split(':')
     inst_name=instli[0]
     inst_ver=instli[1]
     upstream_file=conf.li[inst_name].getUpFile()

     print upstream_file
     print inst_name
     print inst_ver

     if d["status"] == "start":
          print "start action"
          startInstance(inst_name,d["id"],inst_ver)
          conf.show_config(inst_name,inst_ver)
          conf.generate_upstrean(inst_name,d["id"],inst_ver,upstream_file)
          executor.nginxRestart()
     elif d["status"] == "die":
          print "die action"
          stopInstance(inst_name,d["id"],inst_ver)
          conf.show_config(inst_name,inst_ver)
          conf.generate_upstrean(inst_name,d["id"],inst_ver,upstream_file)
          executor.nginxRestart()


