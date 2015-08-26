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
            c = imgtype(sec,ip,port,image,version,onstart)
            tup = {version:c}
            self.li[sec] = tup





    def addInternal(self,inst,id):
        tmp_obj=self.li[inst]
        tmp_obj.addIntIp(inst,id)
        self.li[inst]=tmp_obj

    def show_config_all(self):
        for (char, n) in self.li.items():
	        print "klucz:",char,"wartosc:",n

    def show_config(self,type,version):
        self.li[type][version].showIntIp()




    def generate_upstrean(self,inst,id,inst_ver):
        plik = open('upstream-'+inst + "-" + inst_ver + ".conf", 'w')
        plik.write("upstream-"+inst+"{\r\n")
        c=self.li[inst][inst_ver]
        for (char, n) in c.int_ip.items():
            plik.write("server "+ n +";\r\n")
        plik.write("}")
        plik.close()






