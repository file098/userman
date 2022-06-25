import os, subprocess, shlex
import ui, colors

USERMOD = shlex.split("usermod")

class User:

    username = None
    name = None
    uid = None
    id = None
    home_folder = None
    shell = None
    superuser = False
    groups = []

def check_user_exists(user):
    return os.system(f"id {user} &>/dev/null ") == 0 

def list_usernames():
    # return the list of users present in the user database

    os.system("getent passwd | egrep  '(/bin/bash)|(/bin/zsh)|(/bin/sh)' | cut -f1 -d:")
    print("\n")

def list_users():

    with open("/etc/passwd", 'r') as f: 
            lines = f.readlines()

            userInfo = []
            for line in lines:
                username, sep, tail = line.partition(':')

                userObj = User()

                for i in range(1, 8):
                    cmd = "getent passwd {username}| cut -d: -f{i}".format(username=username, i=i)
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    output = str(p.communicate()[0]).replace("b'","").replace("\\n'","")
                    
                    match i:
                        case 1 :
                            userObj.username = output
                        case 2 :
                            userObj.name = output
                        case 3 :
                            userObj.uid = output
                        case 4 :
                            userObj.id = output
                        case 5 :
                            userObj.name = output
                        case 6 :
                            userObj.home_folder = output
                        case 7:
                            userObj.shell = output

                userInfo.append(userObj)

            f.close()
            ui.print_users(userInfo)

    # return the list of users present in the user database
    # cmd = "getent passwd | egrep  '(/bin/bash)|(/bin/zsh)|(/bin/sh)' | cut -f1 -d:"
    # os.system(cmd)
    # print("\n")

def create_user(username, uuid, group, root, set_password):
    # given an username, the function will create a new user
    # user can choose to create user as root, set password, group and specific user uuid
    # HACK: it's not possible to pass more than on group during the creation

    cmd = shlex.split("useradd")

    args = shlex.split("-d /home/{username} {username}".format(group=group, username=username))
    if (root == "y"):
        args += shlex.split("-r")

    if uuid:
        args += shlex.split("-u {uuid}".format(uuid=uuid))

    group_len = len(group)
    if group_len:
        args += shlex.split("-g {group} ".format(group=group))

    try:
        response = subprocess.check_call(cmd + args, stderr=subprocess.STDOUT)
        create_dir_cmd = shlex.split("mkdir -p /home/{username}".format(username=username))
        subprocess.call(create_dir_cmd)
    except subprocess.CalledProcessError as err:
        ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
        response = err.returncode
        print(response)
    else:
        ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
        if response == 0:
            if (set_password == "y" or set_password == "Y"):
                cmd = shlex.split(f"passwd {username}") 
                subprocess.call(cmd)


def change_username(prev_user, new_user):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename
    cmd = shlex.split("usermod")
    args = shlex.split("-l {new} {old}".format(new=new_user, old=prev_user))

    try:
        response = subprocess.check_call(USERMOD + args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
        response = err.returncode

    match response:
        case 0:
            ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
        case _:
            ui.print_color_msg("change_username failed with the following error:", colors.COLOR_RED)
            print(response)

def change_user_main_group(username, main_group):
    # dato un username e una stringa (nuovo username) modifica il gruppo principale, non vengono fatti controlli sull'esistenza dell'usename

    args = shlex.split("-g {main_group} {username}".format(main_group=main_group, username=username))
    try:
        response = subprocess.check_call(USERMOD + args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
        response = err.returncode
        print(response)
        return False
    else:
        ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
        return True


def change_home_directory(username, path, move_files =False):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa

    #   * mkdir /home/new_home_directory
    #   * chown username:username /home/new_home_directory
    #   * chmod 700 /home/new_home_directory
    #   * usermod --home /home/new_home_directory username
    #   * Change the home directory by editing /etc/passwd
    if check_user_exists(username):
        
        if not os.path.isdir(path):
        # if the passed path doesnt exist, it creates it
            create_dir = "mkdir {path}".format(path=path)
            os.system(create_dir)
        
        # preparing ownership commands
        own_dir_cmd = shlex.split("chown {username}:users {path}".format(username=username, path=path))
        permission_dir_cmd = shlex.split("chmod 700 {path}".format(path=path))
        chg_user_cmd = shlex.split("usermod --home {path} {username}".format(username=username, path=path))
        
        # running above commands 
        subprocess.Popen(own_dir_cmd)
        subprocess.Popen(permission_dir_cmd)
        subprocess.Popen(chg_user_cmd)

        with open("/etc/passwd", 'r') as f,open("/etc/passwd",'w') as o:
            data = f.read()

            # gets user's entry in /etc/passwd
            current_dir_cmd = shlex.split(("getent passwd {username}").format(username=username))

            new_passwd_entry=""
            # current_dir = ""
            for i in range(1, 8):
                # gets entry by entry of the getent passwd command
                cmd = "getent passwd {username} | cut -d: -f{i}".format(username=username, i=i)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                output = str(p.communicate()[0]).replace("b'","").replace("\\n'","")
                
                # /etc/passwd entry that contains home folder
                if i == 6:
                    # current_dir = output
                    output = path

                new_passwd_entry += output
                
                if not i == 7:
                    new_passwd_entry += ":"

            user_passwd_entry = str(subprocess.Popen(current_dir_cmd, stdout=subprocess.PIPE ).communicate()[0]).replace("\\n'", '').replace("b'", "")

            data = data.replace(user_passwd_entry,new_passwd_entry)
            o.write(data)
            o.close()


        args = shlex.split("-d {path} {username}".format(path=path, username=username))
        if move_files: 
            args += shlex.split("-m")
        try:
            response = subprocess.check_call(USERMOD + args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
            response = err.returncode
            print(response)
        else:
            ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
    else:
        ui.print_color_msg("Invalid path", colors.COLOR_RED)


def change_user_uid(username, uid):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename 
    # nemmeno sulla corretteza del uid

    args = shlex.split("-u {uid} {username}".format(uid=uid, username=username))
    try:
        response = subprocess.check_call(USERMOD + args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
        response = err.returncode

    match response:
        case 0:
            ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
        case _:
            ui.print_color_msg("change_user_uid failed with the following error:", colors.COLOR_RED)
            print(response)

def change_user_shell(username, shell):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename 
    
    if os.path.exists(shell):
        args = shlex.split("-s {shell} {username}".format(shell=shell, username=username))
        try:
            response = subprocess.check_call(USERMOD + args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
            response = err.returncode

        match response:
            case 0:
                ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
                return True
            case _:
                
                ui.print_color_msg("change_user_shell failed with the following error:", colors.COLOR_RED)
                print(response)
                return False
    else:
        ui.print_color_msg("Provided shell does not exist on your system", colors.COLOR_RED)
        return False

def delete_user(username, delete_user_home=False):
    # dato un username la funzione controlla l' esistenza dell'username e in caso di corretteza, elimina l'utente
    # non vengono eliminati i dati relativi all'utente

    user = username.strip()
    if check_user_exists(user):

        if delete_user_home: 
            delete = "rm -r /home/{username}".format(username=username)
            confirm_delete = input("Are you sure you want to delete this user? (y/n)\n") == "y"
            confirm_delete and os.system(delete)
        cmd = shlex.split("userdel")
        args = shlex.split("{username}".format(username=username))
        try:
            response = subprocess.check_call(cmd + args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
            response = err.returncode

        match response:
            case 0:
                ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
                return 0
            case _:
                ui.print_color_msg("Error, I can't delete the inserted user", colors.COLOR_RED)
                print(response)
                return response
    else:
        ui.print_color_msg("User does not exist", colors.COLOR_RED)
        return 1
