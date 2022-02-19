import os, argparse

# This daemon handles sending files around the PKB
# No cap, I can just run this from the command line. Pretty legit

# I mean, the basics seem simple enough....? I should probably error check though
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an note to another file")
    parser.add_argument("note", metavar="N", nargs='+')
    parser.add_argument("-f", dest="filenames", nargs='+')
    args = parser.parse_args()
    # This should be a default argument, no flag)

    # This is for writing to the sent files, not reading.
    for filename in args.filenames:
        # I'm just going to assume the file exists for now
        file = open(filename,'a')
        file.write(args.note)
        file.close()

