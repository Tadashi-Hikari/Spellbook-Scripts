# The most essential features are:
# Works on Android/Linux
# Linkbacks & homepage
# Tag linking

import re, os

root_directory = ""
hub_directory = ""
backlink_directory = ""
tag_prefix = "tag-hub-"
backlink_prefix = "backlink-"
# I don't think this will update with the variables. I need to be mindful of this
ignored = [""]
v = False

def verbose(string):
    global v
    if v == True:
        print(string)

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
        if (info[0] == "hub"):
            hub_directory = info[1]
        if (info[0] == "backlink"):
            backlink_directory = info[1]
    file.close()
    # Update the directories to NOT crawl
    ignored = [root_directory + hub_directory, root_directory + backlink_directory]

def crawl_spellbook(directory):
    contents = os.listdir(directory)

    global ignored

    for path in contents:
        absolute = directory+path
        ignore = False

        #ignore those directories
        for item in ignored:
            if (absolute.find(item) != -1):
                verbose("ignoring directory")
                ignore = True

        if(ignore == True):
            continue
        elif(os.path.isfile(absolute)):
            verbose("checking path "+absolute)
            check_file(absolute)
        else:
            verbose("checking path "+absolute)
            crawl_spellbook(absolute+"/")

def check_file(path):
    if (path.endswith("org") or
            path.endswith("md")):
        check_for_links(path)
        check_for_tags(path)

def check_for_links(path):
    global root_directory, backlink_directory, backlink_prefix
    # This is for org mode
    link_regex = "\[{2}.+\]{1,2}"
    filename = "\[{2}\S+?\]{1}"

    if (os.path.isdir(root_directory + backlink_directory) == False):
        os.mkdir(root_directory + backlink_directory)

    regex = re.compile(link_regex)
    subregex = re.compile(filename)
    file = open(path, 'r+')

    verbose("checking "+path+"for links")

    for line in file:
        match_object = regex.search(line)
        verbose("checking line: "+ line)
        if (match_object == None):
            verbose("No link was found")
            continue
        else:
            verbose("A link was found: "+match_object.group())
            match_sub = re.compile(subregex)
            thing = match_sub.search(match_object.group())
            linked_file = thing.group().strip("[").strip("]")
            verbose("The sublink is:"+linked_file.removeprefix("./"))
            backlink_file = backlink_prefix + linked_file.removeprefix("./")
            backlink(path, backlink_file)
    file.close()

# I need to find better names for these things. The need to be UIDs
# I am just going to append-the-path to make them unique, since it's not supposed to be human manipulated anwyay
def backlink(path,backlink_file):
    global root_directory, backlink_directory
    backlink_path = root_directory+backlink_directory+backlink_file

    if (os.path.isfile(backlink_path) == False):
        file = open(backlink_path, 'w+')
    else:
        file = open(backlink_path, 'r+')

    link_path = "[[" + path + "]]"
    for line in backlink_file:
        if (line.strip("\n") == link_path.strip("\n")):
            file.close()
            return
    # Make it, ya know, linkable
    file.write(link_path+"\n")
    file.close()

# This is where the header/footer portion should come in. I don't want to constantly make new tag stuff
def check_for_tags(path):
    # This is for org mode
    tag_regex = ":(\S+?:)+"
    regex = re.compile(tag_regex)

    global root_directory, hub_directory
    if (os.path.isdir(root_directory + hub_directory) == False):
        os.mkdir(root_directory + hub_directory)

    file = open(path, 'r')

    verbose("checking "+path+" for tags")

    for line in file:
        verbose("checking line: "+ line)
        match_object = regex.search(line)
        if (match_object == None):
            verbose("No tag was found")
            continue
        else:
            verbose("A tag was found: "+match_object.group())
            for tag in match_object.group().split(":"):
                if (tag != ""):
                    check_tag_hub(tag)
                    link_tags(tag,path)
    file.close()

def check_tag_hub(tag):
    global hub_directory, tag_prefix
    filename = "tag-hub-main.org"

    if (os.path.isfile(hub_directory + filename) == False):
        file = open(hub_directory + filename, 'w+')
    else:
        file = open(hub_directory + filename, 'r+')


    for line in file:
        if (line.strip("\n") == "[[./"+tag_prefix+tag+".org]["+tag+"]]".strip("\n")):
            file.close()
            return 0
    # since the tag isn't in here, add it. It should link to the localized tag_hub
    file.write("[[./" + tag_prefix + tag + ".org][" + tag + "]]\n")
    file.close()

# This creates a link TO the local tag hub in the existing tagged file
def link_tags(tag,tagged_file_path):
    global hub_directory, tag_prefix

    if (os.path.isfile(hub_directory + tag_prefix + tag + ".org") == False):
        file = open(hub_directory + tag_prefix + tag + ".org", 'w+')
    else:
        file = open(hub_directory + tag_prefix + tag + ".org", 'r+')

    for line in file:
        if (line.strip("\n") == "[["+tagged_file_path+"]]".strip("\n")):
            file.close()
            return 0
    file.write("[[" + tagged_file_path + "]]\n")
    file.close()

if __name__ == '__main__':

    config()
    crawl_spellbook(root_directory)
    # Run the command daemon. I'll touch these all up later
    command = ["python","command_daemon.py"]
    ##command = [python,"git_daemon.py"]
    ##command = ["python","quicknote_daemon.py"]
