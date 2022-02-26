import sys
import termcolor
from command import moduleCommand, profileCommand, initModuleLoading
import message



commandList = {}
version = "alpha v1.0.5"
globals()["version"] = version
globals()["listModule"] = []
listModule = []
success = message.Success()
warnings = message.Warning()
errors = message.Error()


def printHeader():
    header = """
 __  __        _                                         _     
|  \/  |  ___ | |_  __ _  _ __ ___    ___   _ __  _ __  | |__  
| |\/| | / _ \| __|/ _` || '_ ` _ \  / _ \ | '__|| '_ \ | '_ \ 
| |  | ||  __/| |_| (_| || | | | | || (_) || |   | |_) || | | |
|_|  |_| \___| \__|\__,_||_| |_| |_| \___/ |_|   | .__/ |_| |_|  
                                                 |_|             """ + str(version)
    print(header)

def printHelp(command):
    print("\r\nMetamorph V" + str(globals()["version"]) + """, Website Scanning Tool
General help about commands
    
        
""" + str(listModule[0].description) + '\n\n' + str(listModule[1].description))


def printShell():
    try:
        print("\nmetamorph$: ", end='')
        return 0
    except Exception as errShell:
        errors.getMessage(errShell)
        return -1



def main():
    initModuleLoading()
    moduleCom = moduleCommand("module", """MODULE:
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
    profileCom = profileCommand("profile", """PROFILE:
        Manage scanning profiles
        load <profile name>:
            load scanning profile
        status,show:
            show actual profile settings
        export <new profile name>:
            save actual settings
        help:
            show this help""")
    listModule.insert(0, moduleCom)
    listModule.insert(1, profileCom)
    command_list = {"help": printHelp,
                    "h": printHelp,
                    "module": moduleCom.callCommand,
                    "m": moduleCom.callCommand,
                    "profile": profileCom.callCommand,
                    "p": profileCom.callCommand}
    command = ""

    while command != "exit" and command != "quit":
        printShell()
        command = input()
        command = command.lower()
        command = command.strip()
        commandArg = command.split(' ')
        commandArg = [i for i in commandArg if i != '']
        if len(command) != 0:
            try:
                command_list[commandArg[0]](commandArg)
            except KeyError:
                msgErr = errors.getMessage("Command Not Recognized !" + '\nCommand : ' + str(command))
                print(msgErr)
            except Exception as error:
                msgErr = errors.getMessage("An error Occured !" + '\nCommand : ' + str(command) + "\nException : " + str(error))
                print(msgErr)



    return 0



if __name__ == '__main__':
    printHeader()
    globals()["loadedModule"] = None
    globals()["version"] = version
    try:
        main()
    except KeyboardInterrupt:
        print(termcolor.colored("\r\nGoodBye !", 'green'))
        sys.exit(0)
    except Exception as err:
        print(errors.getMessage(err))
        sys.exit(0)
