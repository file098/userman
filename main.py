import os, sys
import ui



def main():
    print('''
    Welcome to UserMan
    ''')
    choices = ["User management", "Folders management", "Backups"]
    ui.print_choises(choices)
    choise = input("What should I do?\n")


    if(choise == "0" | "User management"):
        ui.user_management_choises()
    elif(choise == "1" | "Folders management"):
        ui.folders_management_choises()
    elif(choise == "2"):
        print("3");
    else:
        print("wrong choice");
        

def create_user(username, uuid, group, system, set_password):
    cmd = "useradd -d /home/{username} {username}".format(group=group, username=username)
    if system:
        cmd += "-r"
    if uuid:
        cmd += "-u {uuid}".format(uuid=uuid)
    group_len = len(group)
    if group_len:
        if group_len == 1:
            cmd += "-g {group}".format(group=group)
        else:
            cmd += "-G "
            for elem in group:
                cmd += "{elem},".format(elem=elem)

    if os.system(cmd) == 0:
        print(f"Operation successful, created user {username}")
        if set_password:
            os.system(f"passwd {username}")
        return 1;
    else:
        print("Operation failed")
        return 0;


def delete_user(username):
    if os.system(f"getent passwd {username}"):
        return os.system(f"userdel {username}") == 0
    else:
        print("Error, I can't delete the user inserted")
