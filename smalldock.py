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
     #print cnf
     ip_wew=cnf['NetworkSettings']['IPAddress']
     conf.li[inst][inst_ver].showIntIp
     conf.li[inst][inst_ver].addIntIp(id,ip_wew)

     if conf.li[inst][inst_ver].ip_pool[0] is not "0":
         ip_zew=conf.li[inst][inst_ver].getFreeIp()
         print 'Assign external IP: ' + ip_zew
         executor.addIpRule(ip_wew,ip_zew)
         conf.li[inst][inst_ver].addExtIp(id,ip_zew)
     else:
         print "This machine have no IP assigned"


def stopInstance(inst,id,version):
     ip_wew=conf.li[inst][version].getIntIP(id)
     print ip_wew
     conf.li[inst][version].removeIntIp(id)
     if conf.li[inst][inst_ver].ip_pool[0] is not "0":
         ip_zew=conf.li[inst][inst_ver].getExtIp(id)
         print 'Deassign external IP: ' + ip_zew
         executor.delIpRule(ip_wew,ip_zew)
         conf.li[inst][version].removeExtIp(id)
     else:
         print "This machine have no IP to remove"


#print type(conf.li["centos"]["latest"])
#print_config()
#getSystemContainters()
#conf.show_config("centos","latest")

def runInstances(inst,ver,count):
    print 'Start instance ' + inst + ":" + ver, count
    for c in range(0,int(count)):
        container = dock.create_container(image=inst + ":" + ver,command='/bin/sleep 30' )
        response = dock.start(container=container.get('Id'))
        print response

for (i, n) in conf.li.items():
    for (c,d) in n.items():
        thread = threading.Thread(target=runInstances, args=(i,c,d.toStartInst()))
        thread.daemon = True
        thread.start()






getSystemContainters()





for line in dock.events():
     #print(json.dumps(json.loads(line), indent=4))
     #d=json.dumps(json.loads(line), indent=4)
     d=json.loads(line)
     #print d["status"]

     instli=d["from"].split(':')
     inst_name=instli[0]
     inst_ver=instli[1]


     if d["status"] == "start":
          print "start action"
          startInstance(inst_name,d["id"],inst_ver)
          conf.show_config(inst_name,inst_ver)
          conf.generate_upstrean(inst_name,d["id"],inst_ver)
     elif d["status"] == "die":
          print "die action"
          stopInstance(inst_name,d["id"],inst_ver)
          conf.show_config(inst_name,inst_ver)
          conf.generate_upstrean(inst_name,d["id"],inst_ver)



