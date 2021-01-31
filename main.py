import subprocess
import os
import sys
#this function checks if a program is installed or not
def is_installed(name):
    try:
        subprocess.Popen([name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).communicate()
    except OSError:
        return False
    return True
#Jan 30 19:56:58 ubuntu su: FAILED SU (to root) exp on pts/1
def authlog_reader(name):
    try:
        f = open(sys.argv[1], "r")
        for x in f:
            print(x)
    except FileNotFoundError:
        print("Couldn't find file, please enter full path!")
authlog_reader(sys.argv[1])
#print(sys.argv[1])