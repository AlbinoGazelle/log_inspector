import sys
#helper function for eliminating unique values from a list
def get_unique(list):
    unique = []
    for x in list:
        if x not in unique:
            unique.append(x)
    return unique
#Jan 30 19:56:58 ubuntu su: FAILED SU (to root) exp on pts/1
def authlog_reader(name):
    password_attempt = []
    failed_attempt = []
    command_attempt = []
    print("Printing useful information: \n")
    try:
        f = open(sys.argv[1], "r")
        for x in f:
            txt = x.split(" ")
            #get lines for failed SU attemps
            if "FAILED" in x:
                failed_attempt.append(txt[9])
                print(f"user: {txt[10]} {txt[9]} attempted to SU to user: {txt[8].rstrip(')')} at {txt[0], txt[1], txt[2]}")
            #get lines for commands that are executed
            elif "COMMAND" in x and "incorrect password" not in x:
                command_attempt.append(txt[7])
                print(f"user: {txt[7]} executed: {x[x.find('COMMAND'):len(x) - 1]} at {txt[0], txt[1], txt[2]}")
            #get lines for failed password attempts
            elif "incorrect password attempts" in x:
                password_attempt.append(txt[7])
                print(f"user: {txt[7]} tried to execute: {x[x.find('COMMAND'):len(x) - 1]} at {txt[0], txt[1], txt[2]} as the {txt[18]}")
    except FileNotFoundError:
        print("Couldn't find file, please enter full path!")
    except PermissionError:
        print("Insufficient permissions to read this file, maybe run as sudo?")
    print(" ")
    print("Printing how many times each user did something:\n")
    #print the number of times users did something
    unique_users_password = get_unique(password_attempt)
    for x in unique_users_password:
        print(f"{x} attempted to execute a command {password_attempt.count(x)} times ")

    unique_users_failed = get_unique(failed_attempt)
    for x in unique_users_failed:
        print(f"{x} attempted to SU to a user {failed_attempt.count(x)} times ")

    unique_users_command = get_unique(command_attempt)
    for x in unique_users_command:
        print(f"{x} executed a command {command_attempt.count(x)} times ")

if len(sys.argv) !=2:
    print("usage: ./inspector.sh path_to_log_file")
    exit()
elif "auth.log" in sys.argv[1]:
    authlog_reader(sys.argv[1])