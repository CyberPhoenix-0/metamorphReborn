import termcolor
from module import moduleStruct
import json
import message
import os
import sys

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
        if moduleSelected is not None:
            if moduleSelected in moduleList.keys():
                print(moduleList[moduleSelected].getHelp())
                return 0
            else:
                print(errors.getMessage("Parameter \'" + str(moduleSelected) + "\' not recognized !"))
                return 0
        else:
            print(self.description)
            return 0


class moduleCommand(commandStruct):

    def __init__(self, name, desc):
        if globals()["initedVar"]:
            commandStruct.__init__(self, name, desc)
            globals()["moduleCommandInstance"] = self
        else:
            errors.getMessage("Modules not inited")

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
                    if selectedModuleName in moduleList.keys():  #if module exists
                        if selectedModuleName in globals()["loadedModule"].keys():
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
                            print(errors.getMessage("Module selected not loaded"))
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
        args of module loading, contains load in 1, moduleName in 2, and moduleArgs in 3 -> ...
        :return:
        """
        if command[2] not in globals()["loadedModule"].keys():
            globals()["loadedModule"][command[2]] = (moduleList[command[2]])
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
        if len(globals()["loadedModule"]) > 0:
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
        if command is not None:
            if command[2] in moduleList.keys():
                if command[2] in globals()["loadedModule"].keys():
                    print(globals()["loadedModule"][command[2]].getStrPrintArgs())
                    return 0
                else:
                    print(warnings.getMessage("Module specified not loaded !"))
                    return -1
            else:
                print(errors.getMessage("Module selected does not exists"))
                return -1
        else:
            if globals()["loadedModule"] is None or len(globals()["loadedModule"]) == 0:
                msg = warnings.getMessage("No Module loaded !")
                print(msg)
                return 0
            else:
                for i, j in globals()["loadedModule"].items():
                    print(str(j.getStrPrintArgs()))
                return 0

    def moduleVar(self, command):
        """
        Change var of selected setting to input value
        :param command:
        :return:
        """
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
                print(success.getMessage("Successfully updated " + str(selectedOption) + " to " + str(NewValue)))
            except (ValueError, TypeError):
                print(errors.getMessage("Parameter " + str(selectedOption) + " need " + str(OldValueType) + " but " + str(NewValueType) + " given"))
                return -1
            except Exception as err:
                print(errors.getMessage("\n" + str(err) + "\n"))
                return -1
        else:
            print(errors.getMessage("No Module Selected !\r\nSelect one first before changing settings."))
            return -1



class profileCommand(commandStruct):

    def __init__(self, name, desc):
        commandStruct.__init__(self, name, desc)
        globals()["profileCommandInstance"] = self

    def callCommand(self, command):
        """
        General handler of parameters
        :param command:
        Original command split by ' '
        :return:
        """
        if len(command) > 1:
            if command[1] == "help":  #handle Help command
                self.printHelp(None)
            elif command[1] == "load":  #handler load command
                if len(command) > 2:
                    self.profileLoad(command)
                else:
                    print(warnings.getMessage("Missing ScanProfileName parameter !"))
                    return -1
            elif command[1] == "show" or command[1] == "status":  #handle show command
                self.profileShow()
            elif command[1] == "save":
                print(warnings.getMessage("Did you mean   p export ?"))
                return 0
            elif command[1] == "export":
                if len(command) > 2:
                    self.profileExport(command[1:])
                else:
                    print(warnings.getMessage("Missing newProfileName parameter !"))
                    return -1
            else:
                print(errors.getMessage('\'' + str(command[1]) + "\' option not recognized"))
                self.printHelp(None)
                return -1
        else:
            self.printHelp(None)
            return 0

    def profileLoad(self, command):
        """

        :param command:
        profile to load in command[1]
        :return:
        """
        try:
            if ".json" in str(command[2]):
                profilePath = "profiles/" + str(command[2])
            else:
                profilePath = "profiles/" + str(command[2] + ".json")
            profileFile = open(profilePath, 'r')
            jsonConfig = json.load(profileFile)
            if len(jsonConfig) >= 2:
                for i in range(1, len(jsonConfig)):
                    moduleName = jsonConfig[i][0]
                    loadCommand = ["m", "load", jsonConfig[i][0]]
                    if moduleName not in globals()["loadedModule"].keys():
                        globals()["moduleCommandInstance"].moduleLoad(loadCommand)
                    else:
                        print(warnings.getMessage(str(moduleName) + " module already loaded, updating parameters"))
                        return -1
                    argDico = jsonConfig[i][1]
                    for arg, val in argDico.items():
                        varCommand = ["m", "var", jsonConfig[i][0], arg, str(val)]
                        globals()["moduleCommandInstance"].moduleVar(varCommand)
            else:
                print(errors.getMessage("Invalid Profile"))
                return -1
        except FileNotFoundError:
            print(errors.getMessage("Profile not found, choose an existing file in profiles/ directory"))
            return -1
        except Exception as errMessage:
            print(errors.getMessage("An error occured while loading profile!\n" + str(errMessage)))
            return -1

    def profileShow(self):
        """
        No need of arguments
        :return:
        """
        if len(globals()["loadedModule"]) != 0:
            for i, j in globals()["loadedModule"].items():
                trayCount = len(j.printName)
                print(termcolor.colored(j.printName, "green"))
                print(termcolor.colored('-'*trayCount, "green"))
                print(j.getStrPrintArgs())
                print('\r\n')
                return 0
        else:
            print(warnings.getMessage("No module Loaded !"))
            return -1

    def profileExport(self, command):
        """
        Export actual profile to file
        :param command:
        name of New Profile
        :return:
        """
        if len(globals()["loadedModule"]) != 0:
            try:
                profileConfig = [command[1]]
                for i, j in globals()["loadedModule"].items():
                    profileConfig.append((i, j.argList))
                jsonProfileConfig = json.dumps(profileConfig, indent=4)
                if ".json" not in profileConfig[0]:
                    profilePath = open("profiles/" + str(profileConfig[0]) + ".json", 'w')
                else:
                    profilePath = open("profiles/" + str(profileConfig[0]), 'w')
                profilePath.write(jsonProfileConfig)
                print(success.getMessage("Exported " + str(profileConfig[0])))
                return 0
            except (FileExistsError, FileNotFoundError):
                print(errors.getMessage("Can't write profile Config"))
                return -1
            except Exception as err:
                print(errors.getMessage(str("Fatal Error Occured " + err)))
                return -1
        else:
            print(warnings.getMessage("No module Loaded !"))
            return 0



class sysCommand(commandStruct):

    def __init__(self, name, desc):
        commandStruct.__init__(self, name, desc)
        globals()["profileCommandInstance"] = self

    def callCommand(self, command):
        """
        General handler of parameters
        :param command:
        Original command split by ' '
        :return:
        """
        if len(command) > 1:
            ' '.join(command[1:])
            return os.system(' '.join(command[1:]))
        else:
            self.printHelp(None)
            return 0

    






moduleList = {}
globals()


def initModuleLoading():
    try:
        files = os.listdir("moduleConfig/")
        holder = {}
        for file in files:
            path = "moduleConfig/" + file
            jsonFile = open(path, "r")
            moduleConfig = json.load(jsonFile)
            holder[moduleConfig[0]] = moduleStruct(name=moduleConfig[0], printName=moduleConfig[1],
                                                   path=moduleConfig[2], desc=moduleConfig[3],
                                                   args=moduleConfig[4])
            initVar(holder[moduleConfig[0]])
        globals()["initedVar"] = True
        print(termcolor.colored("[*]Success : Loaded Module Database !", 'blue'))
        return 0
    except FileNotFoundError:
        print(errors.getMessage("Can't open module Configs directory"))
        sys.exit(-1)


def initVar(module):
    moduleList[module.name] = module
    return 0

