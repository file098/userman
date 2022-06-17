import os, subprocess, shlex
import ui, colors

USERMOD = shlex.split("usermod")

def check_user_exists(user):
    return os.system(f"id {user} &>/dev/null ") == 0 

def list_users():
    # return the list of users present in the user database
    cmd = "getent passwd | egrep  '(/bin/bash)|(/bin/zsh)|(/bin/sh)' | cut -f1 -d:"
    os.system(cmd)
    print("\n")

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
        subprocess.call("mkdir -p /home/{username}".format(username=username))
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
    else:
        ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)


def change_home_directory(username, path, move_files =False):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa

    create_dir = "mkdir {path}".format(path=path)
    own_dir = "chown {username}:{username} {path}".format(username=username, path=path)
    permission_dir = "chmod 700 {path}".format(path=path)
    chg_user = "usermod --home {path} {username}".format(username=username, path=path)
    
    with open("/etc/passwd", 'r') as f,open("/etc/passdtest",'w') as o:
        data = f.read()

        cmd = shlex.split(("getent passwd {username}").format(username=username))

        user_passwd_entry = str(subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()[0]).replace("/n'", '').replace("b'", ""))

        user_entry = "test:x:1001:100::/home/test:/run/current-system/sw/bin/bash"
        new_entry = user_passwd_entry.replace("::", '').replace()
        
        data = data.replace(user_passwd_entry,new_entry)
        o.write(data)
        o.close()

    # TODO: I need to do this procedure to change home directory
    # * Run the following commands to do it.

    #   * mkdir /home/new_home_directory
    #   * chown username:username /home/new_home_directory
    #   * chmod 700 /home/new_home_directory
    #   * usermod --home /home/new_home_directory username
    #   * Change the home directory by editing /etc/passwd

    if os.path.isdir(path) and user.check_user_exists(username):

        args = shlex.split("-d {path} {username}".format(path=path, username=username))
        if move_files: 
            args += shlex.split("-m")
        try:
            print(USERMOD + args)
            response = subprocess.check_call(USERMOD + args,shell=True, stderr=subprocess.STDOUT)
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
    # nemmeno sull'esistenza della directory TODO: aggiungere controllo

    args = shlex.split("-s {shell} {username}".format(shell=shell, username=username))
    try:
        response = subprocess.check_call(USERMOD + args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        ui.print_color_msg("Operation failed with the following error:", colors.COLOR_RED)
        response = err.returncode

    match response:
        case 0:
            ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
        case _:
            ui.print_color_msg("change_user_shell failed with the following error:", colors.COLOR_RED)
            print(response)


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
