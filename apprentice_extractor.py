import argparse, re, json

start_regex = ".*#=.*"
end_regex = ".*=#.*"
id_regex = "-\w+(-{1}|(\+[\w|\$]+\+*)+-{1})"

def extract_paragraph(line):
    # This seems pretty straight forward
    return line

def extract_sentence(line):
    global id_regex

    sentences = re.split("\. | \! | \?", line)
    id_matcher = re.compile(id_regex)
    for s_index, sentence in enumerate(sentences):
        match_object = id_matcher.search(sentence)
        if (match_object != None):
            return sentences[s_index]

# Should it extract ahead, or behind
def extract_token(line):
    global id_regex
    tokens = re.split("\s",line)
    id_matcher = re.compile(id_regex)
    for t_index,token in enumerate(tokens):
        match_object = id_matcher.search(token)
        if(match_object != None):
            # Return the token just before the syntax
            return tokens[t_index-1]

def extract_block(index,lines):
    # I've change this so that block just returns the end point
    end = check_for_end(index, lines)
    return end
    #start = check_for_start(index, lines)
    # if a matcher finds an end before a start, or vice versa, it knows it's not within a block
    #if(start < end):
        #block = lines[start:end]
    #else:
        #return ""
    #return block

def check_for_start(index, lines):
    global start_regex, end_regex
    good_matcher = re.compile(start_regex)
    bad_matcher = re.compile(end_regex)

    while (index > 0):
        line = lines[index]
        good_match = good_matcher.match(line)
        bad_match = bad_matcher.match(line)
        if (good_match != None):
            return index
        elif (bad_match != None):
            return len(lines)
        index = index-1
    return 0

def check_for_end(index, lines):
    global start_regex, end_regex
    good_matcher = re.compile(end_regex)
    bad_matcher = re.compile(start_regex)

    while (index < len(lines)):
        line = lines[index]
        good_match = good_matcher.match(line)
        bad_match = bad_matcher.match(line)
        if (good_match != None):
            return index+1
        elif(bad_match != None):
            return 0
        index = index + 1
    return len(lines)-1

def expand_json(json_file):
    return(json.loads(json_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a token, sentence, block, or paragraph from a file")
    # This should be the default behavior
    parser.add_argument("-s", dest="sentence")
    parser.add_argument("-p", dest="paragraph")
    parser.add_argument("-t", dest="token")
    # Block is the only one that will take JSON
    parser.add_argument("-b", dest="block")
    args = parser.parse_args()


    # Block just needs to return the end information
    if(args.block == True):
        lines = json.loads(args.block)
        extracted = extract_block(lines)
        print(extracted)
    else:
        if(args.sentence != None):
            extracted = extract_sentence(args.sentence)
        elif(args.paragraph != None):
            extracted = extract_paragraph(args.paragraph)
        elif(args.token != None):
            extracted = extract_token(args.token)
