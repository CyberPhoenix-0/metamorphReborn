import datetime
from socket import *
import sys
from termcolor import colored
from datetime import date
import os

"""
Metamorph NetScan Module
V2
Argument : host, FromPort, ToPort, debugLevel
Desc : Network Scanning tool, host in argument, fromPort and toPort argument optional. If fromPort and toPort specified, both needs to be int. If not, netScan use 0 and 1000 by default
Syntaxe : module netscan <host> [<fromPort> <toPort> <debug lvl>]
Info : fromPort and toPort need to be specified to use debug

"""

def scan(host, up, down, debug):
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
    return writeRes(openedPort, host, up, down, debug)



def writeRes(openedPort, host, up, down, debug):
    nowTime = str(datetime.datetime.today().time()).split('.')[0].replace(':', '.')
    fileName = "netscan_" + str(date.today()) + '_' + str(nowTime) + ".report"
    actualPath = os.path.realpath(__file__)
    filePath = os.path.join(actualPath + "/../results/", fileName)
    print(filePath)
    header = "Metamorph Report for Netscan\nArguments:\nrhost : " + str(host) + "\nFrom Port : " + str(up) + "\nTo Port : " + str(down) + "\nDebug Level : " + str(debug)
    report = open(str(filePath), 'w')

    if len(openedPort) == 0:
        report.write(header + "\n\n" + "No Opened Port on desired range")
    else:
        report.write(header + "\n\n" + str(openedPort))
    return fileName


def main():
    if len(sys.argv) < 2:
        return "NetScan : This module needs at least one argument, see help"
    else:
        if len(sys.argv) == 2:
            return scan(sys.argv[1], 0, 1000, 0)
        elif len(sys.argv) == 3:
            return "NetScan : Missing toPort argument, see help"
        elif len(sys.argv) == 4:
            try:
                fromPort = int(sys.argv[2])
                toPort = int(sys.argv[3])
                return scan(sys.argv[1], fromPort, toPort, 0)
            except Exception as err:
                return "NetScan : An error occured." + str(err)
        elif len(sys.argv) == 5:
            try:
                fromPort = int(sys.argv[2])
                toPort = int(sys.argv[3])
                dbgLvl = int(sys.argv[4])
                return scan(sys.argv[1], fromPort, toPort, dbgLvl)
            except Exception as err:
                return "NetScan : An error occured." + str(err)
    return -1


if __name__ == '__main__':
    try:
        reportPathFile = main()
        sys.exit(0)
    except (KeyboardInterrupt, InterruptedError):
        print(colored("NetScan : Scan Stopped !", 'red'))
        sys.exit(-1)
    except Exception as err:
        print(colored("Netscan : Fatal Error Occured", 'red'))
        print(str(err))
        sys.exit(-1)
