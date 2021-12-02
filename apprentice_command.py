import argparse, re, json, subprocess

# This is expecting to work w/ extractor, I'd think

def find_command(lines):
    command_regex = "-\w+(-{1}|(\+[\w|\$]+\+*)+-{1})"
    regex = re.compile(command_regex)

    for index,line in enumerate(lines):
        command_match = regex.search(line)
        if(command_match != None):
            return (command_match.group())

# We are just pulling out the simple command here. Extractor is for other manipulations to non-command data
def print_lines(line,match):
    return line[0:match.start()] + line[match.end():len(line) - 1]

def print_command(match):
    command = match.group().strip("-").split("+")

# command is a string or list of strings
def check_command_file(command):
    commands_file = "temp"
    file = open(commands_file, "r")
    for line in file:
        split = line.split("=")
        if(command == split[0]):
            return split[1]

# it expects string/json input
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run", dest="command")
    parser.add_argument("-d", dest="data")
    parser.add_argument("extract", dest="extract")
    parser.add_argument("expand", dest="expand")
    parser.add_argument("-i", dest="ignore", action="store_true")
    args = parser.parse_args()

    # Decode the lines via JSON
    if(args.block != None):
        lines = json.dumps(args.block)
    if(args.expand == True):
        find_command(lines)
    else:
        # run the command
        subprocess.run(args.command,args.block)