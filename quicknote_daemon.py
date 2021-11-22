# When exactly should I call this file?
# I suppose it doesn't matter if I make a million of them

import os, datetime

# update quicknote_hub
def manage_quicknote_hub():
    print

# This just simply renames the file
if __name__ == '__main__':
    title = "QuickNote.md"
    # This is datetime...
    timetitle = datetime.datetime.now().strftime("%Y%m%d%%H%M%S")+".md"
    os.rename(title,timetitle)

    #check for a quicknote tag
    # add if it doesn't exist
    # Any reason I *shouldn't* put this in a quicknote folder?
    file = open(timetitle,"a+")
    # just append a simple quicknote tag
    file.write(":quicknote:")
