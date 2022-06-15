import os, datetime
import ui, colors, user

def backup_user(username, exclude_list=[]):
    date = datetime.datetime.now()
    cmd = f"tar -zcvpf /backup/{username}-backup-" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + f".tar.gz /home/{username}"
    if len(exclude_list) > 0:
        print("Lista vuota")
    print(cmd)