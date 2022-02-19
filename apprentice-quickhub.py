import subprocess

if __name__ == "__main__":
  file = open("./tag-hub/tag-hub-main.org")
  values = ""
  records = []
  for line in file:
    record = line.strip().strip('[[').strip(']]').split("][")
    records.append(record)
    values = values+','+record[1]
  values = values.strip(',')
  subprocess.run(["termux-dialog","spinner","-v",values,"-t","Access Topic"])