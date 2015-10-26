#!/usr/bin/python

import os
import json
import docker
import executor
import threading
import time
import datetime
import os
import string
import random

from configurator import ConfigFactory


dock = docker.Client(base_url='unix://var/run/docker.sock', version='1.19', timeout=10)
print "number of containers = ", len(dock.containers(all))
print "docker version is python ", docker.version

conf = ConfigFactory()
conf.show_config_all()


def instance_monitor():
    while True:
        time.sleep(15)
        for (c,d) in conf.li.items():
            if d.toStartInst() != 0:
                thread = threading.Thread(target=runInstances, args=(c, d.getVersion(), d.toStartInst(),d.getVolumes(),d.getHosts(),d.getHostname(),d.getEnv(),d.getPrivileged()))
                thread.daemon = True
                thread.start()
            else:
                print "All Instances OK"




def getSystemContainters():
        sc=dock.containers()
        for l in sc:

            instli=l["Image"].split(':')
            print instli
            inst_name=instli[0]
            inst_ver=instli[1]
            id=l["Id"]
            startInstance(inst_name,id,inst_ver)



def print_config():
     print conf
     print dock.containers()

tab_iptable=executor.parseIpTables()

#print tab_iptable

def startInstance(inst,id,inst_ver):
     if inst in conf.li.keys():
         cnf=dock.inspect_container(id)
         ip_wew=cnf['NetworkSettings']['IPAddress']
         conf.li[inst].showIntIp()
         conf.li[inst].addIntIp(id,ip_wew)
         if conf.li[inst].ip_pool[0] is not "0":
             if tab_iptable.has_key(ip_wew):
                 print "Iptables rule already set"
                 ip_zew=tab_iptable[ip_wew]
                 conf.li[inst].addExtIp(id,ip_zew)
             else:
                  ip_zew=conf.li[inst].getFreeIp()
                  print 'Assign external IP: ' + ip_zew
                  executor.addIpRule(ip_wew,ip_zew)
                  conf.li[inst].addExtIp(id,ip_zew)
         else:
             print "This machine have no IP assigned"
     else:
         print "There is no configuration for: " + inst

def stopInstance(inst,id,version):
     if inst in conf.li.keys():
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
     else:
         print "There is no configuration for: " + inst










def runInstances(inst, ver, count, vol, hosts, hostname, env, privileged):
    if inst in conf.li.keys():
        print 'Start instance ' + inst + ":" + ver, count
        for c in range(0,int(count)):
            print 'create container!'
            print vol

            #container=dock.create_container(image=inst + ":" + ver,hostname=None, user=None,
                         #detach=False, stdin_open=False, tty=False,
                         #mem_limit=None, ports=None, environment=None,
                         #dns=None, volumes=vol, volumes_from=None,
                         #network_disabled=False, name=None, entrypoint=None,
                         #cpu_shares=None, working_dir=None, domainname=None,
                         #memswap_limit=None, cpuset=None, host_config=None,
                         #mac_address=None, labels=None, volume_driver=None)
            #container = dock.create_container(image=inst + ":" + ver, command='/bin/sleep 90', volumes=['/mnt/vol1', '/mnt/vol2'])


            #,volumes_from=[{"/tmp"},{"/test"}],volume_driver="local"
            #print 'start container with params:'
            #print container.get('volumes')
            # binds={
            #     '/test':
            #         {
            #             'bind': '/mnt/test',
            #             'ro': False
            #         },
            #     '/var/www':
            #         {
            #             'bind': '/mnt/vol1',
            #             'ro': True
            #         }
            # }
            #response = dock.start(container=container.get('Id'),binds={
            #                                   '/home/user1/': {
            #                                        'bind': '/mnt/vol2',
            #                                        'mode': 'rw',
            #                                    },
            #                                    '/var/www': {
            #                                        'bind': '/mnt/vol1',
            #                                        'mode': 'ro',
            #                                     }}
            #                                  )
            #print response

            #volumes workaround

            if hostname != "":
                #hostname='-h '.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(N))
                hostname = "-h " + hostname

            volumes_dirs = ""
            for v in vol:
                if v != "":
                    volumes_dirs = volumes_dirs + " -v " + v
            now_is = datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
            volumes_dirs=volumes_dirs.replace("[date]",now_is)
            print volumes_dirs
            host_tab = ""
            for h in hosts:
                if h != "":
                    host_tab = host_tab + " --add-host " + h

            env_tab = ""
            for e in env:
                if e != "":
                    env_tab = env_tab + " -e " + e

            prv=""
            print "privileged:" + privileged
            if privileged != "":
                prv = " --privileged "

            command = "docker run -d " + env_tab + hostname + volumes_dirs + host_tab + prv +" " + \
                      inst + ":" + ver
            print command
            os.system(command)

    else:
        print "There is no configuration for: " + inst




getSystemContainters()




for (c,d) in conf.li.items():
   thread = threading.Thread(target=runInstances, args=(c,d.getVersion(),d.toStartInst(),d.getVolumes(),d.getHosts(),d.getHostname(),d.getEnv(),d.getPrivileged()))
   thread.daemon = True
   thread.start()






for (inst_name,d) in conf.li.items():
    upstream_file=conf.li[inst_name].getUpFile()
    conf.generate_upstrean(inst_name,d.showIntIp(),d.getVersion(),upstream_file)

executor.nginxRestart()


mon_thread = threading.Thread(target=instance_monitor)
mon_thread.daemon = True
mon_thread.start()



conf.show_config_all()

for line in dock.events():
     d=json.loads(line)
     if d["status"] == "start":
          if ':' in d["from"]:
             instli=d["from"].split(':')
             inst_name=instli[0]
             inst_ver=instli[1]
          else:
             inst_name=d["from"]
             inst_ver='rebuild_start_die'

          if inst_name in conf.li.keys():
              print "start action"
              upstream_file=conf.li[inst_name].getUpFile()
              startInstance(inst_name,d["id"],inst_ver)
              conf.show_config(inst_name,inst_ver)
              conf.generate_upstrean(inst_name,d["id"],inst_ver,upstream_file)
              executor.nginxRestart()
          else:
              print "There is no configuration for: " + inst_name + ":" + inst_ver
     elif d["status"] == "die":
          if ':' in d["from"]:
             instli=d["from"].split(':')
             inst_name=instli[0]
             inst_ver=instli[1]
          else:
             inst_name=d["from"]
             inst_ver='rebuild_start_die'

          if inst_name in conf.li.keys():
              print "die action"
              upstream_file=conf.li[inst_name].getUpFile()
              stopInstance(inst_name,d["id"],inst_ver)
              conf.show_config(inst_name,inst_ver)
              conf.generate_upstrean(inst_name,d["id"],inst_ver,upstream_file)
              executor.nginxRestart()
          else:
              print "There is no configuration for: " + inst_name + ":" + inst_ver


