import os
import json
import docker
from configurator import ConfigFactory

dock = docker.Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)
print "number of containers = ", len(dock.containers(all))
print "docker version is python ", docker.version

conf = ConfigFactory()
conf.show_config_all()


def print_config():
     print conf


def startInstance(inst,id):
     print inst
     cnf=dock.inspect_container(id)
     print cnf
     ip_wew=cnf['NetworkSettings']['IPAddress']
     conf.li[inst].showIntIp
     conf.li[inst].addIntIp(id,ip_wew)



def stopInstance(inst,id):
     conf.li[inst].removeIntIp(id)

print_config()

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
          startInstance(inst_name,d["id"])
          conf.show_config(inst_name)
          conf.generate_upstrean(inst_name,d["id"])
     elif d["status"] == "die":
          print "die action"
          stopInstance(inst_name,d["id"])
          conf.show_config(inst_name)
          conf.generate_upstrean(inst_name,d["id"])



     #print d



     #print d[0]['status']


#from smalldock.application import Application


# if __name__ == '__main__':
#   app = Application({
#        'config': './config.file',
#       'docker_host': '127.0.0.1',
#         'docker_port': '4243',
#        }
#    })
#    app.start(8888)
