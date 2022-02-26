import datetime
import subprocess
import sys
import time

from termcolor import colored

import asyncio.subprocess


async def run(cmd,arg):
    a = subprocess.run(['dir'], shell=True,capture_output=True)
    print("result : " + str(a))
    print(type(a))
    eee = a.stdout
    print(str(eee))


def main():
    return asyncio.run(run('powershell', 'dir'))


if __name__ == '__main__':
    try:
        print(main())
    except KeyboardInterrupt:
        print(colored("Test : Scan Stopped !", 'red'))
    except Exception as err:
        print(err)
