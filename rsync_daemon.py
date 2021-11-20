import subprocess, re, os

command = ["rsync"]

hub_directory = ""
host = "192.168.0.1"

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

def call_simple_spellbook_daemon():
  print("JK I don't want to integrate it that much yet")

def scan_public_hub():
  temp_var = "tag-hub-public"
  file = open(temp_var,'r')
  for line in file:


# This maybe should be its own daemon
def make_website_hubs():


# This maybe should be its own daemon
def make_website_backlinks():

if __name__ == "__main__":
  tag_hub = open("garden-hub.org")
  # This should read from a config file

  for index,line in enumerate(tag_hub):
    if(index == 0):
      command.add(host+":"+line)
    else:
      command.add(":"+line)

  subprocess.run(command)
