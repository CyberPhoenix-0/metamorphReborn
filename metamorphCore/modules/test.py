import datetime
import sys
import time

from termcolor import colored




def main():
    return str(sys.argv[1]) + " " + str(time.time())

if __name__ == '__main__':
    try:
        print(main())
    except:
        print(colored("Test : Scan Stopped !",'red'))