import subprocess, datetime

# Does this really need to do much more? I just need to be sure it's running in right directory
if __name__ == "__main__":
    command = ["git","add","-A"]
    subprocess.run(command)

    time = datetime.datetime.now().strftime("%Y%m%d%:%H%M%S")
    command = ["git","commit","-m","autoupdated by spellbook on "+time]
