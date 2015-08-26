__author__ = 'ajafo'

class imgtype:
    "Class for get type from config"



    def __init__(self, name,ip,port,image,version,onstart):
         self.name = name
         self.ip_pool = ip.split(',')
         self.port = port
         self.image = image
         self.int_ip = {}
         self.version = version
         self.ip_counter=-1
         self.ext_ip = {}
         self.onstart = onstart

    def addExtIp(self,id,ip):
        self.ext_ip[id]=ip

    def removeExtIp(self,id):
        if id in self.ext_ip:
            del self.ext_ip[id]
        else:
            print 'This machine has no external ip'

    def addIntIp(self,id,ip):
        self.int_ip[id]=ip

    def getIntIP(self,id):
        return self.int_ip[id]

    def showIntIp(self):
        print self.int_ip

    def removeIntIp(self,id):
        if id in self.int_ip:
            del self.int_ip[id]
        else:
            print "There is no registered machine with " + id

    def getExtIp(self,id):
        return self.ext_ip[id]

    def getFreeIp(self):
        self.ip_counter=self.ip_counter + 1
        if self.ip_counter == len(self.ip_pool):
            self.ip_counter = -1
            return self.ip_pool[self.ip_counter]
        else:
            return self.ip_pool[self.ip_counter]

    def countInstances(self):
        return len(self.int_ip)

    def toStartInst(self):
        if len(self.int_ip) == 0:
            return self.onstart
        elif len(self.int_ip) <= self.onstart:
            ile=self.onstart - len(self.int_ip)
            return ile
        else:
            print "It's enough instances"