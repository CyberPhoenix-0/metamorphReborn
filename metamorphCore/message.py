from termcolor import colored

class message:

    type = ""

    def __init__(self, type):
        self.type = type


class Warning(message):

    header = colored("[!]Warning : ", 'yellow')

    def __init__(self):
        message.__init__(self, "Warning")

    def getMessage(self, content):
        return colored(self.header + " " + content + " !")


class Error(message):
    header = colored("[X]Error : ", 'red')

    def __init__(self):
        message.__init__(self, "Error")

    def getMessage(self, content):
        return colored(self.header + " " + content + " !")


class Success(message):
    header = colored("[OK]Success : ", 'green')

    def __init__(self):
        message.__init__(self, "Success")

    def getMessage(self, content):
        return colored(self.header + " " + content + " !")
