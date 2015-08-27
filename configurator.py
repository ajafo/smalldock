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
            if active == "1":
                c = imgtype(sec,ip,port,image,version,onstart,upfile)
                tup = {version:c}
                self.li[sec] = tup
            else:
                print "Found not active configuration: " + image + ":" + version + " " + ip + " " + onstart





    def addInternal(self,inst,id):
        tmp_obj=self.li[inst]
        tmp_obj.addIntIp(inst,id)
        self.li[inst]=tmp_obj

    def show_config_all(self):
        for (char, n) in self.li.items():
	        print "key: ",char,"value: ",n

    def show_config(self,type,version):
        self.li[type][version].showIntIp()




    def generate_upstrean(self,inst,id,inst_ver,upstream_file):
        inst2=inst.replace('/','-')
        print "generate conf file: "
        print inst2
        print inst_ver
        #plik = open('upstream-'+inst2 + ".conf", 'w')
        plik = open(upstream_file,'w')
        plik.write("upstream "+inst2+"{\r\n")
        c=self.li[inst][inst_ver]
        if not c.int_ip.items:
            plik.write("server 127.0.0.1;\r\n")
        else:
            for (char, n) in c.int_ip.items():
                print "Add server: " + n
                plik.write("server "+ n +";\r\n")
            plik.write("}")
        plik.close()







