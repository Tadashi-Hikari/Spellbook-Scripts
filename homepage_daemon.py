import os

# I am just going to make a markor AND an emacs homepage

tags_link = ""
contacts_link = ""
new_journal_entry = ""
recent_notes_link = ""
quicknote_link = ""
search_link = ""

def config():
    global tags_link, new_journal_entry, recent_notes_link, quicknote_link, search_link
    root_directory = ""

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
            tags_link = root_directory+info[1]+"tag-hub-main.org"
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

def convert_to_markdown(line):
    print("Nothing to do yet")

if __name__ == "__main__":
    config()
    markdown_file = open("homepage.md",'w+')
    org_file = open("homepage.org",'w+')

    org_file.write("[["+tags_link+"][Tags]]")
    markdown_file.write("[Tags]("+tags_link+")")