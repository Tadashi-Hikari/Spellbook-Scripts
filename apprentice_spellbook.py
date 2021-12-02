import argparse, subprocess, json

# meant to be run from cli to enchant spellbook (config)
# What does this do?

# As much as possible, I'd like for this to be the 'smart' daemon. the others have no context


# Print the configuration for spellbook on the command line (or to a file)
import re


def list_config():
    print("Not yet implemented")

# append something to one of the lists (alias, ignored, etc)
def append():
    print("Not yet implemented")

def convert_to_json():
    print("Not yet implemented")

def convert_from_json():
    print("Not yet implemented")

if __name__ == "__main__":
    print("Not yet implemented")

    parser = argparse.ArgumentParser()
    # add something to something
    parser.add_argument("-a", dest="add", nargs="+")
    # the list to add something to
    parser.add_argument("-l", dest="list", nargs="+")
    parser.add_argument("-d", dest="display", action="store_true")

    # It will be overwritte w/ the end product
    file = open("file","w+")
    lines = file.readlines()

    end_line = 0
    command = ""
    for index,line in enumerate(lines):
        # This should be pulled from the extractor conf file
        start_regex = ".*#=.*"
        extract_matcher = re.compile(start_regex)
        # In case we've already checked a block
        if(index < end_line):
            continue
        # We've found an extractable portion, do special stuff for the chunk
        # Shit, I don't think I need to do ALL of this unless it's like, SEND or some crap
        if(extract_matcher.search(line) != None):
            # convert the lines to go over text stream
            relevant_lines = lines[index:len(lines)-1]
            text_data = json.dumps(relevant_lines)
            # Pass along all the lines
            process = subprocess.Popen(["python3", "apprentice_extractor.py", "-b", text_data], stdout=subprocess.PIPE)
            # This shouldbe the index for the end of the extraction block
            end_line = int(process.communicate()[0].decode("utf-8").strip())
            print("Block ends on line",end_line)
            # Send the extracted lines, to do whatever it needed it for
            for i,l in enumerate(lines[index:end_line]):
                # remove commands from the line
                process = subprocess.Popen(["python3", "apprentice_command.py","extract",l], stdout=subprocess.PIPE)
                stripped_line = process.communicate()[0].decode("utf-8").strip()
                # Found the first (and only) command
                if(stripped_line != ""):
                    # expand and capture the found command
                    process = subprocess.Popen(["python3, apprentice_command.py","expand",l])
                    command = process.communicate()[0].decode("utf-8").strip()
                    # Replace the command line w/ a clean line
                    relevant_lines[i] = stripped_line
                    # Since that is the *only* relevant command, we can move on now
                    break
            # Since it's known by now all lines are good, expand everything else in them
            for i,l in enumerate(lines[index:end_line]):
                # Expand the line
                process = subprocess.Popen(["python3", "alias_command.py", l])
                expanded_line = process.communicate()[0].decode("utf-8").strip()
                relevant_lines[i] = expanded_line
            # The text should be cleaned and expanded now
            prepared_data = json.dumps(relevant_lines)
            # And do with it whatever needed to be done
            subprocess.run(["python3","apprentice_command.py","run",command,"-d",prepared_data])

