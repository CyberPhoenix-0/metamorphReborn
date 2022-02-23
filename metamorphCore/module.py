class moduleStruct:

    name = ""
    printName = ""
    path = ""
    description = ""
    argList = {}

    def __init__(self, name, printName, path,desc, args):
        self.name = name
        self.printName = printName
        self.path = path
        self.description = desc
        self.argList = args

    def getStrArgs(self):
        arg = ""
        for j in self.argList.values():
            arg = arg + str(j) + ' '
        return arg

    def getHelp(self):
        return self.description

    def printArgs(self):
        strArgs = ""
        for i,j in self.argList.items():
            strArgs = strArgs + str(i) + "   " + str(j) + "\n"
        return strArgs