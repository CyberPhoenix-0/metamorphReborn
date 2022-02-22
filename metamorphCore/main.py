import sys,os
from command import module,profile

from termcolor import colored


commandList = {}
version = "alpha v1.0.0"
globals()["loadedModule"] = None



def printHelp(command):
    print("\r\nMetamorph V" + str(globals()["version"]) + """, Website Scanning Tool
General help about commands
    
    MODULE:
        handler Scannings Modules
        list:
            list all modules
        load:
            load selected module if exists
        help:
            show this help or show help of specified module
    
    PROFILE:
        Manage scanning profiles
        load <profile name>:
            load scanning profile
        status,show:
            show actual profile settings
        save <new profile name>:
            save actual settings
        help:
            show this help
        
    """)


def printShell():
    try:
        print("\nmetamorph$: ", end='')
        return 0
    except:
        return -1



def main():

    moduleCom = module("module", """MODULE:
        Manage and Use Scannings Modules
        status:
            show settings about selected module
        load:
            load selected module if exists
        run:
            run selected module
        list:
            list all modules
        help:
            show this help or show help of specified module
        """)
    profileCom = profile("profile","""PROFILE:
        Manage scanning profiles
        load <profile name>:
            load scanning profile
        status,show:
            show actual profile settings
        save <new profile name>:
            save actual settings
        help:
            show this help""")

    commandList = {"help": printHelp, "module": moduleCom.callCommand, "m": moduleCom.callCommand, "profile": profileCom.callCommand}
    command = ""

    while command != "exit" and command != "quit":
        printShell()

        command = input()
        command = command.lower()
        commandArg = command.split(' ')
        command = command.strip()
        if len(command) != 0:
            try:
                commandList[commandArg[0]](commandArg)
            except Exception as err:
                print(err)
                msgErr = colored("Command Not Recognized !" + '\nCommand : ' + str(command),'red')
                print(msgErr)


    return 0



if __name__ == '__main__':
    globals()["loadedModule"] = None
    globals()["version"] = version
    try:
        main()
    except:
        print(colored("\r\nGoodBye !",'green'))
        sys.exit(0)
