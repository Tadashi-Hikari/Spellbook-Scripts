# When exactly should I call this file?
# I suppose it doesn't matter if I make a million of them

import os, datetime

# This just simply renames the file
if __name__ == '__main__':
    title = "QuickNote.md"
    timetitle = datetime.datetime.now().strftime("%Y%m%d%%H%M%S")+".md"
    os.rename(title,timetitle)

    #check for a quicknote tag
    # add if it doesn't exist
    file = open(timetitle,"a+")
    file.write(":quicknote:")
