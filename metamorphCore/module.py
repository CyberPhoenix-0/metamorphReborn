import os
import json
import sys
import command
import message

success = message.Success()
warnings = message.Warning()
errors = message.Error()

class moduleStruct:
    name = ""
    printName = ""
    path = ""
    description = ""
    argList = {}

    def __init__(self, name, printName, path, desc, args):
        self.name = name
        self.printName = printName
        self.path = path
        self.description = desc
        self.argList = args

    def getStrCommandArgs(self):
        arg = ""
        for j in self.argList.values():
            arg = arg + str(j) + ' '
        return arg

    def getHelp(self):
        return self.description

    def getStrPrintArgs(self):
        from termcolor import colored
        strArgs = colored("Parameter : Value\r\n-----------------\n", 'green')
        for i, j in self.argList.items():
            strArgs = strArgs + str(i) + "  :  " + str(j) + "\n"
        return strArgs

    def run(self):
        pathModule = self.path
        moduleCommand = "python " + pathModule + ' ' + self.getStrCommandArgs()
        print(moduleCommand)
        os.system(moduleCommand)

    def getJsonDict(self):
        moduleLoadedList = [self.name, self.printName, self.path, self.description, self.argList]
        return moduleLoadedList



def moduleExport(moduleObject):
    try:
        file = open("moduleConfig/" + str(moduleObject.name) + ".json", "w")
        jsonConfig = json.dumps(moduleObject.getJsonDict(), sort_keys=True, indent=4)
        file.write(jsonConfig)
        print(success.getMessage("Exporting " + str(moduleObject.name) + ".json"))
    except Exception as err:
        print(errors.getMessage(str(err)))
        return err

