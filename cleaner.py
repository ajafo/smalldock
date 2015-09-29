__author__ = 'ajafo'



import docker
import os

dock = docker.Client(base_url='unix://var/run/docker.sock', version='1.19', timeout=10)


idli={}

def getSystemContainters():
        sc=dock.containers()
        for l in sc:
            id=l["Id"]
            #print id
            cnf=dock.inspect_container(id)
            ip_wew=cnf['NetworkSettings']['IPAddress']
            idli[ip_wew]=id
        return idli


def delIpRule(ip_wew,ip_zew):
    TheCommand = '/sbin/iptables -t nat -D POSTROUTING -p all -s '+ ip_wew + ' -j SNAT --to-source ' + ip_zew
    print TheCommand
    os.system(TheCommand)



def getIpRules():
    TheCommand = "/sbin/iptables -t nat --list | grep SNAT | tr -s ' '| cut -d ' ' -f4,6 > start_rules.txt"
    os.system(TheCommand)


def parseIpTables():
    getIpRules()
    iptable={}
    with open("start_rules.txt", "r") as f:
        for tmpline in f:
            cutstring=tmpline.split('to:')
            cutstring[0]=cutstring[0][:-1]
            cutstring[1]=cutstring[1][:-1]
            iptable[cutstring[0]]=cutstring[1]

    return iptable

def clearRules():
    for (k, v) in tab_iptable.items():
	    #print "key: ",k,"value: ",v
        if dock_table.has_key(k):
            print "Machine with ip "+ k +" is working"
        else:
            delIpRule(k,tab_iptable[k])

getIpRules()
tab_iptable=parseIpTables()
print "***tab iptable **"
print tab_iptable

print "***docker containers***"
dock_table=getSystemContainters()
print dock_table

clearRules()

