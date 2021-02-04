import sys

print_check = False
if("-v" in sys.argv):
        print_check =  True
if(print_check == False):
    print("Use the -v flag to increase verbositity and display what each user did!\nExample: ./inspector -v path_to_log\n")

#helper function for getting unique values from a list
def get_unique(list):
    unique = []
    for x in list:
        if x not in unique:
            unique.append(x)
    return unique
#main function for reading /var/log/auth.log
def authlog_reader(name):
    password_attempt = []
    failed_attempt = []
    command_attempt = []
    auth_failure = []
    ssh_failure = []
    try:
        f = open(name, "r")
        for x in f:
            txt = x.split()
            #get lines for failed SU attemps
            if "FAILED" in x:
                failed_attempt.append(txt[9])
                if(print_check): 
                    print(f"user: {txt[9]} attempted to SU to user: {txt[8].rstrip(')')} at {txt[0], txt[1], txt[2]}")
            #get lines for commands that are executed
            elif "COMMAND" in x and "incorrect password" not in x:
                #fix weird colon issue I was getting in 20.04
                if ":" in x:
                    txt[5] = txt[5].replace(":", "")
                command_attempt.append(txt[5])
                if(print_check):
                    print(f"user: {txt[5]} executed: {x[x.find('COMMAND'):len(x) - 1]} at {txt[0], txt[1], txt[2]}")
            #get lines for failed password attempts
            elif "incorrect password attempts" in x:
                password_attempt.append(txt[5])
                if(print_check):
                    print(f"user: {txt[5]} tried to execute: {x[x.find('COMMAND'):len(x) - 1]} at {txt[0], txt[1], txt[2]} as the {txt[16]}")
            elif "authentication failure" in x and "sshd" not in x:
                auth_failure.append(txt[14])
                if(print_check):
                    print(f"{txt[14]} failed to authenticate as another user!")
            elif "failed password" and "sshd" in x:
                ssh_failure.append(txt[12])
                if(print_check):
                    print(f"user: {txt[10]} attempted to ssh from the IP address: {txt[12]} at {txt[0], txt[1], txt[2]}")
    except FileNotFoundError as e:
        print("Couldn't find file, please enter full path! Error: " + e)
        exit()
    except PermissionError as e:
        print("Insufficient permissions to read this file, maybe run as sudo? Error: "+e)
        exit()

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

    unique_users_auth = get_unique(auth_failure)
    for x in unique_users_auth:
        print(f"{x} tried authenticating as a user {auth_failure.count(x)} times")

if len(sys.argv) <2:
    print("usage: ./inspector.sh path_to_log_file")
    exit()
elif "auth.log" in sys.argv[len(sys.argv) - 1]:
    authlog_reader(sys.argv[len(sys.argv) - 1])