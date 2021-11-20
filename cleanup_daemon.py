import re, os

# crawl backlink to make sure links still exist
# crawl tag hubs to make sure tags still exist

root_directory = ""
hub_directory = ""
backlink_directory = ""
tag_prefix = "tag-hub-"
backlink_prefix = "backlink-"
# I don't think this will update with the variables. I need to be mindful of this
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
        if (info[0] == "hub"):
            hub_directory = info[1]
        if (info[0] == "backlink"):
            backlink_directory = info[1]
    file.close()
    # Update the directories to NOT crawl
    ignored = [root_directory + hub_directory, root_directory + backlink_directory]

def crawl_links():
    global backlink_directory, root_directory
    contents = os.listdir(root_directory + backlink_directory)

    link_syntax_regex = "\[{2}.+\]{1,2}"
    filename = "\[{2}\S+?\]{1}"
    full_link_searcher = re.compile(link_syntax_regex)
    sub_link_searcher = re.compile(filename)

    for filename in contents:
        file = open(filename,'r+')
        for line in file:
            match_object = full_link_searcher.search(line)
            if(match_object.group() != None):
                sub_match_object = sub_link_searcher.search(line)
                linking_file = sub_match_object.group().strip("[").strip("]")
                linked_file = filename.strip("backlink-link")+".org"
                check_file_links(linked_file,linking_file)
        file.close()

# Check if X file is being linked to from file Y
def check_file_links(likned_file,linking_file):
    file = open(linking_file,'r+')

    link_syntax_regex = "\[{2}.+\]{1,2}"
    filename = "\[{2}\S+?\]{1}"
    full_link_searcher = re.compile(link_syntax_regex)
    sub_link_searcher = re.compile(filename)

    for line in file:
        match_object = full_link_searcher.search(line)
        if(match_object != None):
            sub_match_object = sub_link_searcher.search(line)
            # This wont work ouright this way. I need to retain the original file data for the backlink file name
            formatted_link = sub_match_object.group().strip("[").strip("]")

# This generally seems like it will work fine. I need to figure out how to remove that line
def validate_tag_hub():
    global hub_directory, root_directory, tag_prefix
    contents = os.listdir(root_directory + hub_directory)

    for filename in contents:
        current_tag = filename.strip(tag_prefix)
        file = open(filename,'r+')
        for line in file:
            check_file = check_tag_links(current_tag,line)
            if(check_file == True):
                continue
        if(check_file == False):
            print("It needs to remove this line")
            # remove line

# Check if the tags linking to the tag hub still exist
def check_tag_links(current_tag,path):
    tag_regex = ":(\S+?:)+"
    regex = re.compile(tag_regex)

    exists = False

    file = open(path, 'r+')

    for line in file:
        print("checking line:", line)
        match_object = regex.search(line)
        if (match_object == None):
            print("No tag was found")
            continue
        else:
            print("A tag was found:", match_object.group())
            for tag in match_object.group().split(":"):
                if (tag == current_tag):
                    file.close()
                    # it exists. No reason to change anything
                    return 1
            # it didn't exist. Delete the link from the tag_hub
            return 0
    file.close()
