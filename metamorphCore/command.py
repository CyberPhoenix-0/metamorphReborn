from module import moduleStruct
import os
from termcolor import colored
import json


globals()["loadedModule"] = {}

class commandStruct:

    names = []
    description = ""
    calledCommand = []

    def __init__(self,name,desc):
        self.names = [name]
        self.description = desc


    def printHelp(self,module):
        if module != None:
            print(moduleList[module].getHelp())
            return 0
        print(self.description)
        return 0


class module(commandStruct):


    moduleList = {}

    def __init__(self,name,desc):
        commandStruct.__init__(self,name,desc)
        self.moduleList = initVar()

    def callCommand(self,command):
        """
        :param command:
        command is the splited by ' ' table of the original command.
        module help -> ["module","help"]
        :return:
        """
        self.calledCommand = command
        if len(self.calledCommand) > 1:
            if self.calledCommand[1] == "help":
                if len(self.calledCommand) > 2:
                    if self.calledCommand[2] in moduleList.keys():
                        return self.printHelp(self.calledCommand[2])
                    else:
                        print(colored("Error : Module " + str(self.calledCommand[2]) + " not found.", 'red'))
                        self.moduleEnumerate()
                        return -1
                else:
                    return self.printHelp(None)
            elif self.calledCommand[1] == "load":
                if len(self.calledCommand) > 2:
                    if self.calledCommand[2] in moduleList.keys():
                        return self.moduleLoad(self.calledCommand[1:])
                    else:
                        return print(colored("Error : Module " + str(self.calledCommand[2]) + " does not exists.",'red'))
                else:
                    print(colored("Error : Module is missing",'red'))
                    return self.printHelp(None)
            elif self.calledCommand[1] == "list":
                return self.moduleEnumerate()
            elif self.calledCommand[1] == "run":
                return self.moduleRun()
            elif self.calledCommand[1] == "status":
                return self.moduleStatus()
            elif self.calledCommand[1] == "var":
                return self.moduleVar(command[1:])
            elif self.calledCommand[1] == "unload":
                return self.moduleUnload(command[1:])

            else:
                print("Error : \'" + str(self.calledCommand[1]) + "\' option not recognized !")
                self.printHelp(None)
        else:
            self.printHelp(None)


    def moduleLoad(self,command):
        """

        :param command:
        args of module loading, contains load in 0, moduleName in 1, and moduleArgs in 2 -> ...
        :return:
        """
        if command[1] not in globals()["loadedModule"].keys():
            globals()["loadedModule"][command[1]] = (self.moduleList[command[1]])
            try:
                msg = colored("Module " + globals()["loadedModule"][command[1]].name + " loaded !", 'green')
                print(msg)
            except:
                msg = colored("Failed loading module " + command[1] + " !", 'red')
                print(msg)
        else:
            msg = colored("Module " + globals()["loadedModule"][command[1]].name + " already loaded !", 'yellow')
            print(msg)

    def moduleUnload(self,command):
        try:
            del globals()["loadedModule"][command[1]]
            msg = colored("Module " + command[1] + " unloaded !", 'green')
            print(msg)
        except:
            msg = colored("Module " + command[1] + " not loaded !", 'yellow')
            print(msg)


    def moduleRun(self):
        if type(globals()["loadedModule"]) == moduleStruct:
            pathModule = globals()["loadedModule"].path
            moduleCommand = "python " + pathModule + ' ' + globals()["loadedModule"].getStrArgs()
            print(moduleCommand)
            os.system(moduleCommand)
        else:
            return "No module Loaded, load a module first !"

    def moduleEnumerate(self):
        """
        print a list of existing modules
        :return:
        """
        print(colored("Metamorph modules list :","green"))
        for i in moduleList.keys():
            print(str(i))

    def moduleStatus(self):
        """
        print settings of current module
        :return:
        """
        if globals()["loadedModule"] is None:
            msg = colored("No Module Selected !",'red')
            print(msg)
        else:
            print(colored("Parameter : Value\r\n-----------------",'green'))
            for i,j in globals()["loadedModule"].argList.items():
                print(str(i) + " : " + str(j))

    def moduleVar(self,command):
        if len(globals()["loadedModule"]) == 0:
            print(colored("No Module Selected !\r\nSelect one first before changing settings.",'red'))
            return -1
        else:
            try:
                oldValue = globals()["loadedModule"].argList[command[1]]
                if type(command[2]) == type(oldValue):
                    globals()["loadedModule"].argList[command[1]] = command[2]
                    print(colored("Successfully updated " + str(command[1]) + " to " + str(command[2]), 'green'))
                    return 0
                else:
                    if type(oldValue) == int:
                        try:
                            newValue = int(command[2])
                            globals()["loadedModule"].argList[command[1]] = newValue
                            print(colored("Successfully updated " + str(command[1]) + " to " + str(newValue), 'green'))
                            return 0
                        except:
                            print(colored("Parameter " + str(command[1]) + " need " + str(type(oldValue)), 'red'))
                            return -1
                    else:
                        print(colored("Parameter " + str(command[1]) + " need " + str(type(oldValue)), 'red'))
                        return -1
            except:
                print(colored("Parameter " + str(command[1]) + " not recognized ", 'red'))
                return -1


class profile(commandStruct):

    def __init__(self, name, desc):
        commandStruct.__init__(self, name, desc)

    def callCommand(self, command):
        """
        General handler of parameters
        :param command:
        Original command split by ' '
        :return:
        """
        self.calledCommand = command
        if len(self.calledCommand) > 1:
            if self.calledCommand[1] == "help":
                self.printHelp(None)
            elif self.calledCommand[1] == "load":
                self.profileLoad(self.calledCommand[1:])
            elif self.calledCommand[1] == "show":
                self.profileShow()
            else:
                self.printHelp(None)
        else:
            self.printHelp(None)

    def profileLoad(self,command):
        """

        :param command:
        profile to load in command[1]
        :return:
        """
        print("Profile Load")

    def profileSave(self,command):
        """

        :param command:
        profile to save in command[1]
        :return:
        """
        print("Profile List")

    def profileShow(self):
        """
        No need of arguments
        :return:
        """
        for i,j in globals()["loadedModule"].items():
            trayCount = len(j.printName)
            print(colored(j.printName,'green'))
            print(colored('-'*trayCount,'green'))
            print(j.printArgs())
            print('\r\n')




moduleList = {}
def initVar():
    netscan = moduleStruct("netscan","Metamorph NetScan Module V1.0","modules/netScan.py","""
Metamorph NetScan Module
V1.0
Argument : host, FromPort, ToPort, debugLevel
Desc : Network Scanning tool, host in argument, fromPort and toPort argument optional. If fromPort and toPort specified, both needs to be int. If not, netScan use 0 and 1000 by default
Syntaxe : module netscan <host> [<fromPort> <toPort> <debug lvl>]
Info : fromPort and toPort need to be specified to use debug

""",{"rhost":"127.0.0.1","fromport":0,"toport":1000,"debuglevel":0})
    moduleList["netscan"] = netscan
    return moduleList