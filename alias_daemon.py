import os, argparse

# This daemon basically just scans a list of predefined 'quick' commands, and formats them if need be
# Should it stdout the alias? This would pipe best to ANYthing
# For now I am lazy, and just kind of want it to call command. Alias will become a proxy for command_daemon though
import re

alias = ""
commands = {}

def config():
    global alias
    conf = "./.spellbook"
    file = ""
    try:
        file = open(conf, 'r')
    except BaseException as err:
        print(err)
    for line in file:
        info = line.strip("\n").split("=")
        if(info[0] == "alias"):
            alias = info[1]
    file.close()

def alias_config():
    global alias, commands

    file = open(alias,'r')
    for line in file:
        command = line.split("=")
        commands[command[0]] = command[1]
    file.close()

# I think command_check should be expecting one token commands, similar to Alias
def command_check(input):
    for command in commands.keys():
        if(input == command):
            return(expand_syntax(commands[input]))
        # this should probably be prefix, not strip
        elif(input.removeprefix("$") == command):
            # I don't know that I need to strip again?
            return(expand_syntax(commands[input.removeprefix("$")]))

def expand_syntax(compressed_command):
    global commands
    var_regex = "\$\(\w+\)"
    variable_finder = re.compile(var_regex)
    match_object = variable_finder.search(compressed_command)
    if(match_object != None):
        match = match_object.group()
        # Replace the matched group
        compressed_command = re.sub(var_regex, commands[match.strip("$(").strip(")").strip("\'")], compressed_command)
        return(expand_syntax(compressed_command))
    else:
        return(compressed_command)

if __name__ == "__main__":
    config()
    alias_config()

    parser = argparse.ArgumentParser(description="an alias function for writing spells")
    parser.add_argument('default',metavar='a')
    # What's special about this?
    parser.add_argument('-c',dest="command",action="store_true")
    args = parser.parse_args()

    #print("Running alias daemon. Input is:",args.default)

    # I think it's a different syntax
    if(args.command == True):
        print(command_check(args.default.strip("\'")))
    else:
        try:
            print(expand_syntax(args.default))
        except KeyError as ke:
            print("There was a key error. variable",ke,"doesn't exist")
