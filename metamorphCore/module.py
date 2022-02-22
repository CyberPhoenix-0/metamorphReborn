class moduleStruct:

    name = ""
    path = ""
    description = ""
    argList = {}

    def __init__(self, name, path,desc, args):
        self.name = name
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
