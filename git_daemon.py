import subprocess

# Does this really need to do much more?
if __name__ == "__main__":
    command = ["git","add","-A"]
    subprocess.run(command)