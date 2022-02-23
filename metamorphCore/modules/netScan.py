from socket import *
import time
import sys
from termcolor import colored

"""
Metamorph NetScan Module
V1.0
Argument : host, FromPort, ToPort, debugLevel
Desc : Network Scanning tool, host in argument, fromPort and toPort argument optional. If fromPort and toPort specified, both needs to be int. If not, netScan use 0 and 1000 by default
Syntaxe : module netscan <host> [<fromPort> <toPort> <debug lvl>]
Info : fromPort and toPort need to be specified to use debug

"""



startTime = time.time()
def scan(host,up,down,debug):
    openedPort = []
    ip = gethostbyname(host)
    for i in range(up, down + 1):
        if debug > 0:
            print('-' + str(i))
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect_ex((ip, i))
        if conn == 0:
            if debug > 0:
                print("--Port " + str(i) + " opened !")
            openedPort.append(i)
        s.close()
    return openedPort



def main():
    if len(sys.argv) < 2:
        return "NetScan : This module needs at least one argument, see help"
    else:
        if len(sys.argv) == 2:
            return scan(sys.argv[1],0,1000,0)
        elif len(sys.argv) == 3:
            return "NetScan : Missing toPort argument, see help"
        elif len(sys.argv) == 4:
            try:
                fromPort = int(sys.argv[2])
                toPort = int(sys.argv[3])
                return scan(sys.argv[1],fromPort,toPort,0)
            except:
                return "NetScan : Invalid argument, see help."
        elif len(sys.argv) == 5:
            try:
                fromPort = int(sys.argv[2])
                toPort = int(sys.argv[3])
                dbgLvl = int(sys.argv[4])
                return scan(sys.argv[1], fromPort, toPort, dbgLvl)
            except:
                return "NetScan : Invalid argument, see help."
    return -1

if __name__ == '__main__':
    try:
        print(main())
    except:
        print(colored("NetScan : Scan Stopped !",'red'))