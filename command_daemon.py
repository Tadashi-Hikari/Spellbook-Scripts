import re, os

# The command daemon crawls spellbook for commands, and executes them
# It will expand commands /w Alias. How to have them talk w/o Athena?
import subprocess

root_directory = ""
hub_directory = ""
backlink_directory = ""
alias_key = ""
ignored = [""]
daemons_directory = ""

def config():
    global root_directory, hub_directory, backlink_directory, alias_key, ignored, daemons_directory

    conf = os.path.expanduser("./.spellbook")
    file = ""
    try:
        file = open(conf, 'r')
    except BaseException as err:
        print(err)
    for line in file:
        info = line.strip("\n").split("=")
        if (info[0] == "root"):
            root_directory = info[1]
        elif (info[0] == "hub"):
            hub_directory = info[1]
        elif (info[0] == "backlink"):
            backlink_directory = info[1]
        elif (info[0] == "commands"):
            # I need to make a global for this
            command_file = info[1]
        elif (info[0] == "daemons"):
            daemons_directory = info[1]
        elif (info[0] == "alias"):
            alias_key = info[1]
    file.close()
    # Update the directories to NOT crawl
    ignored = [root_directory + hub_directory, root_directory + backlink_directory]

# this is the spells (commands) file
def read_commands(commands_file):
    file = open(commands_file,"a+")
    for line in file:
        split = line.split("=")
        # straight forward syntax
        alias = {}
        alias[split[0]] = split[1]

def crawl_spellbook(directory):
    contents = os.listdir(directory)

    global ignored

    for path in contents:
        absolute = directory+path
        ignore = False

        #ignore those directories
        for item in ignored:
            if (absolute.find(item) != -1):
                print("ignoring directory")
                ignore = True

        if(ignore == True):
            continue
        elif(os.path.isfile(absolute)):
            print("checking path", absolute)
            check_file(absolute)
        else:
            print("checking path", absolute)
            crawl_spellbook(absolute+"/")


def check_file(path):
    if (path.endswith("org") or
            path.endswith("md")):
        check_for_commands(path)

def cut_block():
    print("Cutting block")
    # Search back for the start of file, most recent \n\n

def cut_sentence():
    print("Cutting sentence")
    # Take the line or last X lines, find the command, and backtrack to the most
    # recent /n . or otherwise

def cut_all():
    print("Renaming file")
    # I should really just rename the file

# I'm sticking w/ a simple -+- and alias & syntax
def check_for_commands(path):
    command_regex = "-\w+(-{1}|(\+[\w|\$]+\+*)+-{1})"
    lines = [""]

    file = open(path,"r")

    regex = re.compile(command_regex)
    # I should always check for alias on the first token of a command
    for line in file:
        match_object = regex.search(line)
        if (match_object == None):
            lines.append(line)
            continue
        else:
            # When a command is found, break that biddy up, remove it from the file, and check for aliases
            print("command found")
            print(match_object.group())
            # I need to extract and run the command, that way it's no longer in the note
            command = match_object.group().strip("-").split("+")
            lines.append(line[0:match_object.start()] + line[match_object.end():len(line) - 1])
            print(command)
            temp = ""
            for token in command:
                com = ["python3", daemons_directory + "alias_daemon.py", "-c", "\'" + token.strip() + "\'"]
                process = subprocess.Popen(com, stdout=subprocess.PIPE)
                out = process.communicate()[0].decode("utf-8")
                print("Alias returned:", out, end="")
                temp += " " + out.strip()
            print("Full command:", temp)
            # subcommand.run(command)

    file.close()
    file = open(path,'w')
    for line in lines:
        file.write(line)
    file.close()

if __name__ == "__main__":
    config()
    crawl_spellbook(root_directory)
