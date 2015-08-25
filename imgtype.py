__author__ = 'ajafo'

class imgtype:
    "Class for get type from config"



    def __init__(self, name,ip,port,image):
         self.name = name
         self.ext_ip = ip
         self.port = port
         self.image = image
         self.int_ip = {}

    def addIntIp(self,id,ip):
        self.int_ip[id]=ip

    def getIntIP(self,id):
        #ip=self.int_ip[id]
        print "---"
        print self.int_ip
        print "---"
        #return self.int_ip[id]

    def showIntIp(self):
        print self.int_ip

    def removeIntIp(self,id):
        if id in self.int_ip:
            del self.int_ip[id]
        else:
            print "There is no registered machine with " + id

