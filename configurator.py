__author__ = 'ajafo'


import docker
import ConfigParser
from imgtype import imgtype

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class ConfigFactory(object):
    __metaclass__ = Singleton
    li = {}


    def __init__(self):

        settings = ConfigParser.ConfigParser()

        settings.read("smalldock.ini")

        sections = settings.sections()


        for sec in sections:
            image=settings.get(sec,'image')
            ip=settings.get(sec,'ext_ip')
            port=settings.get(sec,'port')
            version=settings.get(sec,'version')
            onstart=settings.get(sec,'onstart')
            active=settings.get(sec,'active')
            upfile=settings.get(sec,'upfile')

            if settings.has_option(sec,'hostname'):
                hostname=settings.get(sec,'hostname')
            else:
                hostname=""


            if settings.has_option(sec,'hosts'):
                hosts=settings.get(sec,'hosts')
            else:
                hosts=""

            if settings.has_option(sec,'volumes'):
                volumes=settings.get(sec,'volumes')
            else:
                volumes=""

            if active == "1":
                c = imgtype(sec,ip,port,image,version,onstart,upfile,volumes,hosts,hostname)
                #tup = {version:c}
                self.li[sec] = c
            else:
                print "Found not active configuration: " + image + ":" + version + " " + ip + " " + onstart





    def addInternal(self,inst,id):
        tmp_obj=self.li[inst]
        tmp_obj.addIntIp(inst,id)
        self.li[inst]=tmp_obj

    def show_config_all(self):
        for (char, n) in self.li.items():
	        print "key: ",char,"value: ",n
                print "IP table for " + char + ":", n.showIntIp()

    def show_config(self,type,version):
        self.li[type].showIntIp()




    def generate_upstrean(self,inst,id,inst_ver,upstream_file):
        inst2=inst.replace('/','-')
        print "Generate conf file for: " + inst2 +":" +  inst_ver

        plik = open(upstream_file,'w')
        plik.write("upstream "+inst2+"{\r\n")
        c=self.li[inst]


        if len(c.int_ip.items()) > 0:
            for (char, n) in c.int_ip.items():
                print "Add server: " + n + " (instance: " + char
                plik.write("server "+ n +":" + c.getPort() + ";\r\n")
        else:
            plik.write("server 127.0.0.1:8080;\r\n")
        plik.write("}")
        plik.close()







