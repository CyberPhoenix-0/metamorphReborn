from module import moduleStruct
import json
import message

success = message.Success()
warnings = message.Warning()
errors = message.Error()
globals()["loadedModule"] = {}

class commandStruct:

    names = []
    description = ""
    calledCommand = []

    def __init__(self, name, desc):
        self.names = [name]
        self.description = desc


    def printHelp(self, moduleSelected):
        if moduleSelected is None:
            if moduleSelected in moduleList.keys():
                print(moduleList[moduleSelected].getHelp())
                return 0
            else:
                print(errors.getMessage("Parameter \'" + str(moduleSelected) + "\' not recognized !"))
                return 0
        else:
            print(self.description)
            return 0


class module(commandStruct):

    moduleList = {}

    def __init__(self, name, desc):
        commandStruct.__init__(self, name, desc)
        self.moduleList = initVar()

    def callCommand(self, command):
        """
        :param command:
        command is the split by ' ' table of the original command.
        module help -> ["module","help"]
        :return:
        """
        self.calledCommand = command
        if len(self.calledCommand) > 1:
            arg1 = self.calledCommand[1]
            if arg1 == "help":
                if len(self.calledCommand) > 2:
                    return self.printHelp(self.calledCommand[2])
                else:
                    return self.printHelp(None)
            elif arg1 == "load":
                if len(self.calledCommand) > 2:
                    if self.calledCommand[2] in moduleList.keys():
                        return self.moduleLoad(self.calledCommand)
                    else:
                        return print(errors.getMessage("Module " + str(self.calledCommand[2]) + " does not exists."))
                else:
                    print(warnings.getMessage("Module is missing"))
                    return self.printHelp(None)
            elif arg1 == "list":
                return self.moduleEnumerate()
            elif arg1 == "run":
                if len(self.calledCommand) > 2:
                    return self.moduleRun(self.calledCommand[2])
                else:
                    return self.moduleRun("all")
            elif arg1 == "status":
                if len(self.calledCommand) > 2:  #if module specified
                    return self.moduleStatus(command)
                else:
                    return self.moduleStatus(None)
            elif arg1 == "var":
                selectedModuleName = self.calledCommand[2]
                if len(self.calledCommand) > 2:  #if module is given
                    if selectedModuleName in self.moduleList.keys():  #if module exists
                        selectedModuleObject = globals()["loadedModule"][selectedModuleName]
                        if len(self.calledCommand) > 3:  # if parameter name is given
                            paraName = self.calledCommand[3]
                            if paraName in selectedModuleObject.argList.keys():  #if parameter exists in module ArgList
                                if len(self.calledCommand) > 4:  #if value given
                                    return self.moduleVar(command)
                                else:
                                    print(warnings.getMessage("Value not specified !"))
                            else:
                                print(errors.getMessage("Parameter \'" + str(paraName) + "\' does not belongs to " + selectedModuleName + " module"))
                        else:
                            print(warnings.getMessage("Missing Parameter Name !"))
                    else:
                        print(errors.getMessage("Module \'" + str(self.calledCommand[2]) + "\' does not exists"))
                else:
                    print(warnings.getMessage("Missing \'module\'"))


            elif arg1 == "unload":
                return self.moduleUnload(command[1:])
            else:
                print(errors.getMessage('\'' + str(self.calledCommand[1]) + "\' option not recognized"))
                self.printHelp(None)
        else:
            self.printHelp(None)


    def moduleLoad(self, command):
        """
        :param command:
        args of module loading, contains load in 0, moduleName in 1, and moduleArgs in 2 -> ...
        :return:
        """
        if command[2] not in globals()["loadedModule"].keys():
            globals()["loadedModule"][command[2]] = (self.moduleList[command[2]])
            try:
                print(success.getMessage("Module " + globals()["loadedModule"][command[2]].name + " loaded !"))
            except KeyError:
                print(errors.getMessage("Failed loading module " + command[2] + " !"))
                return -1
            except Exception as err:
                print(errors.getMessage(str(err) + " ! "))
                return -1
        else:
            msg = warnings.getMessage("Module " + globals()["loadedModule"][command[2]].name + " already loaded !")
            print(msg)


    def moduleUnload(self, command):
        try:
            del globals()["loadedModule"][command[1]]
            msg = success.getMessage("Module " + command[1] + " unloaded")
            print(msg)
        except KeyError:
            msg = warnings.getMessage("Module " + command[1] + " not loaded !")
            print(msg)
        except Exception as err:
            print(errors.getMessage(str(err)))


    def moduleRun(self, moduleToRun):
        """

        :param moduleToRun:
        module param can be 'name of module' to run or 'all' to run all modules loaded
        :return:
        """
        if len(globals()["loadedModule"]) > 1:
            if moduleToRun == "all":
                for moduleToRun in globals()["loadedModule"].values():
                    moduleToRun.run()
            elif moduleToRun in globals()["loadedModule"].keys():
                globals()["loadedModule"][moduleToRun].run()
            else:
                return print(warnings.getMessage("Module does not exists Loaded, load a module first !"))
        else:
            msg = warnings.getMessage("No module Loaded, load a module first or specify 'all' to run whole profile !")
            return print(msg)


    def moduleEnumerate(self):
        """
        print a list of existing modules
        :return:
        """
        print(success.getMessage("Metamorph modules list :"))
        for i in moduleList.keys():
            print(str(i))


    def moduleStatus(self, command):
        """
        print settings of current module
        :return:
        """
        if globals()["loadedModule"] is None or len(globals()["loadedModule"]) == 0:
            msg = warnings.getMessage("No Module Selected !")
            print(msg)
            return 0
        else:
            if command is None:
                for i, j in globals()["loadedModule"].items():
                    print(str(j.getStrPrintArgs()))
                return 0
            else:
                if command[2] in globals()["loadedModule"].keys():
                    print(globals()["loadedModule"][command[2]].getStrPrintArgs())
                    return 0
                else:
                    print(warnings.getMessage("Module specified not loaded !"))


    def moduleVar(self, command):
        """
        Change var of selected setting to input value
        :param command:
        :return:
        """
        print(command)
        selectedModule = command[2]
        selectedOption = command[3]
        OldValueType = type(globals()["loadedModule"][selectedModule].argList[selectedOption])
        NewValueType = type(command[4])
        if len(globals()["loadedModule"]) != 0:
            try:
                if OldValueType != str:
                    NewValue = OldValueType(command[4])
                else:
                    NewValue = command[4]
                globals()["loadedModule"][selectedModule].argList[selectedOption] = NewValue
            except (ValueError, TypeError):
                print(errors.getMessage("Parameter " + str(selectedOption) + " need " + str(OldValueType) + " but " + str(NewValueType) + " given"))
                return -1
            except Exception as err:
                print(errors.getMessage("\n" + str(err) + "\n"))
                return -1
        else:
            print(errors.getMessage("No Module Selected !\r\nSelect one first before changing settings."))
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
            if self.calledCommand[1] == "help":  #handle Help command
                self.printHelp(None)
            elif self.calledCommand[1] == "load":  #handler load command
                self.profileLoad(self.calledCommand[1:])
            elif self.calledCommand[1] == "show":  #handle show command
                self.profileShow()
            elif self.calledCommand[1] == "export":
                if len(self.calledCommand) > 2:
                    self.profileExport(command[1:])
                else:
                    print(warnings.getMessage("Missing newProfileName parameter !"))
            else:
                self.printHelp(self.calledCommand[1])
        else:
            self.printHelp(None)

    def profileLoad(self, command):
        """

        :param command:
        profile to load in command[1]
        :return:
        """
        print("Profile Load  " + str(command))

    def profileSave(self, command):
        """

        :param command:
        profile to save in command[1]
        :return:
        """
        print("Profile List  " + str(command))

    def profileShow(self):
        """
        No need of arguments
        :return:
        """
        if len(globals()["loadedModule"]) != 0:
            for i, j in globals()["loadedModule"].items():
                trayCount = len(j.printName)
                print(success.getMessage(j.printName))
                print(success.getMessage('-'*trayCount))
                print(j.getStrPrintArgs())
                print('\r\n')
        else:
            print(warnings.getMessage("No module Loaded !"))

    def profileExport(self, command):
        """
        Export actual profile to file
        :param command:
        name of New Profile
        :return:
        """
        if len(globals()["loadedModule"]) != 0:
            moduleLoadedList = [command[1]]
            for i, j in globals()["loadedModule"].items():
                moduleLoadedList.append((i, j.argList))

            print(json.dumps(moduleLoadedList, sort_keys=True, indent=4))
        else:
            print(warnings.getMessage("No module Loaded !"))


moduleList = {}
def initVar():
    netscan = moduleStruct("netscan", "Metamorph NetScan Module V1.0", "modules/netScan.py", """
Metamorph NetScan Module
V1.0
Argument : host, FromPort, ToPort, debugLevel
Desc : Network Scanning tool, host in argument, fromPort and toPort argument optional. If fromPort and toPort specified, both needs to be int. If not, netScan use 0 and 1000 by default
Syntaxe : module netscan <host> [<fromPort> <toPort> <debug lvl>]
Info : fromPort and toPort need to be specified to use debug

""", {"rhost": "127.0.0.1", "fromport": 0, "toport": 1000, "debuglevel": 0})
    moduleList["netscan"] = netscan

    xss = moduleStruct("xss", "Metamorph XSS Module V1.0", "modules/xss.py", """
    Input : En argv[1] : Le fichier xml généré par sitemap.py
    Output : Fichier xml "XSS_url.xml" avec des "_" a la place des "." et des "-"
    Metamorph XSS Module
    V1.0
    Argument : xmlFile
    Desc : XSS Scanning tool, xmlFile in argument. XMLFile can be generated by sitemap.py
    Syntaxe : module xss <xmlFile>
    
    """, {"xml": "filePath"})
    moduleList["xss"] = xss

    sitemap = moduleStruct("sitemap", "Metamorph SiteMap Module V1.0", "modules/sitemap.py", """
    Input : argv[1]=URL a scanner
    Output : Fichier XML "url.xml" avec des "_" a la place des "." et des "-"
    Metamorph SiteMap Module
    V1.0
    Argument : url
    Desc : SiteMap Scanning tool, xmlFile in argument
    Syntaxe : module sitemap <url>
    
    """, {"url": "https://google.com"})
    moduleList["sitemap"] = sitemap

    whois = moduleStruct("whois", "Metamorph WhoIs Module V1.0", "modules/whois.py", """
    Input : url en argv[1] de la forme http(s)://(www.)site.com => ()=optionnel
    Output : fichier xml "whois_url.xml" avec des "_" a la place des "." et des "-"
    Metamorph WhoIs Module
    V1.0
    Argument : host
    Desc : Network Scanning tool, url in argument
    Syntaxe : module whois <ulr>

        """, {"url": "https://google.com"})
    moduleList["whois"] = whois

    return moduleList
