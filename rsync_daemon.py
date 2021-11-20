import subprocess, re, os

# This won't full work without a password, and I will need to salt and hash the passwd

upload_files = [""]
root_directory = ""
hub_directory = ""
host = "127.0.0.1"
host_directory = "/var/www/html/"

def config():
  global root_directory, hub_directory, host

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
    if (info[0] == "host"):
      host = info[1]
  print(host)
  file.close()

def call_simple_spellbook_daemon():
  print("JK I don't want to integrate it that much yet")

def scan_public_hub():
  global upload_files

  temp_var = "tag-hub-public"
  file = open(temp_var,'r')
  for line in file:
    filepath = line.strip("[[").strip("]]").strip("\n")
    upload_files.append(filepath)

if __name__ == "__main__":
  config()
  scan_public_hub()

  command = ["rsync"]

  for filepath in upload_files:
      command.append(filepath+" ")

  command.append(["chris@" + host + ":" + host_directory])
  subprocess.run(command)