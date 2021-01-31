import subprocess
import os
import sys




#Jan 30 19:56:58 ubuntu su: FAILED SU (to root) exp on pts/1
def authlog_reader(name):
    try:
        f = open(sys.argv[1], "r")
        for x in f:
            txt = x.split(" ")
            #get lines for failed SU attemps
            if "FAILED" in x:
                print(f"user: {txt[9]} attempted to SU to user: {txt[8].rstrip(')')} at {txt[0], txt[1], txt[2]}")
            elif "COMMAND" in x and "incorrect password" not in x:
                print(f"user: {txt[7]} executed: {x[x.find('COMMAND'):len(x) - 1]} at {txt[0], txt[1], txt[2]}")
            #Jan 31 00:49:07 tryhackme sudo:   albino : 2 incorrect password attempts ; TTY=pts/0 ; PWD=/home/albino/Desktop ; USER=root ; COMMAND=/usr/bin/apt-get install apache2
            elif "incorrect password attempts" in x:
                print(f"user: {txt[7]} tried to execute: {x[x.find('COMMAND'):len(x) - 1]} at {txt[0], txt[1], txt[2]} as the {txt[18]}")
    except FileNotFoundError:
        print("Couldn't find file, please enter full path!")
    except PermissionError:
        print("Insufficient permissions to read this file, maybe run as sudo?")
if len(sys.argv) !=2:
    print("usage: ./inspector.sh path_to_log_file")
    exit()
elif "auth.log" in sys.argv[1]:
    authlog_reader(sys.argv[1])