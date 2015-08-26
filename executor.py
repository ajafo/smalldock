__author__ = 'ajafo'

import os

def getIpRules():
    TheCommand = 'iptables -nvL'
    os.system(TheCommand)

def addIpRule(ip_wew,ip_zew):
    TheCommand = '/sbin/iptables -t nat -I POSTROUTING -p all -s '+ ip_wew + ' -j SNAT --to-source ' + ip_zew
    print TheCommand
    os.system(TheCommand)


def delIpRule(ip_wew,ip_zew):
    TheCommand = '/sbin/iptables -t nat -D POSTROUTING -p all -s '+ ip_wew + ' -j SNAT --to-source ' + ip_zew
    print TheCommand
    os.system(TheCommand)


