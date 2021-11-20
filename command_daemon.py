import re, os

root_directory = ""
hub_directory = ""
backlink_directory = ""
ignored = [""]

def config():
    global root_directory, hub_directory, backlink_directory, ignored

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
    file.close()
    # Update the directories to NOT crawl
    ignored = [root_directory + hub_directory, root_directory + backlink_directory]

def read_commands(commands_file):
    file = open(commands_file,"a+")
    for line in file:
        split = line.split("=")
        # straight forward syntax
        alias = {"":""}
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

def check_for_commands(path):
    command_regex = "-\w+(-{1}|(\+\w+\+*)+-{1})"

    file = open(path,"r")

    regex = re.compile(command_regex)
    # I don't think I need to name it file, but w/e
    # I am sure there is an easier way to do this
    for line in file:
        match_object = regex.search(line)
        if (match_object == None):
            return 0
        else:
            # This is just to see if it works, for now
            print("command found")
            print(match_object.group())
            # I need to extract and run the command, that way it's no longer in the note
            return 1
