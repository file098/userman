import os, datetime, subprocess
import ui, colors, user

def backup_user(username, exclude_list=[], backup_path = "/home/", ):
    date = datetime.datetime.now()
    cmd = f"tar -zcvpf /home/{username}-backup-" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + f".tar.gz /home/{username}"
    if len(exclude_list) >= 0:
        for folders in exclude_list:
            cmd += " --exclude=" + folders + " "
    return subprocess.call(cmd, shell=True)