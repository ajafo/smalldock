__author__ = 'ajafo'

import os

def getIpRules():
    TheCommand = "/sbin/iptables -t nat --list | grep SNAT | tr -s ' '| cut -d ' ' -f4,6 > start_rules.txt"
    os.system(TheCommand)


def addIpRule(ip_wew,ip_zew):
    TheCommand = '/sbin/iptables -t nat -I POSTROUTING -p all -s '+ ip_wew + ' -j SNAT --to-source ' + ip_zew
    print TheCommand
    os.system(TheCommand)


def delIpRule(ip_wew,ip_zew):
    TheCommand = '/sbin/iptables -t nat -D POSTROUTING -p all -s '+ ip_wew + ' -j SNAT --to-source ' + ip_zew
    print TheCommand
    os.system(TheCommand)

def nginxRestart():
    TheCommand = 'service nginx restart'
    print TheCommand
    os.system(TheCommand)


def printIpRules():
    print getIpRules()


def parseIpTables():
    getIpRules()
    iptable={}
    with open("start_rules.txt", "r") as f:
        for tmpline in f:
            cutstring=tmpline.split('to:')
            cutstring[0]=cutstring[0][:-1]
            cutstring[1]=cutstring[1][:-2]
            iptable[cutstring[0]]=cutstring[1]

    return iptable