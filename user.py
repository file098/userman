import os, subprocess, shlex
import ui, colors

USERMOD = shlex.split("usermod")

def check_user_exists(user):
    return os.system(f"id {user} &>/dev/null ") == 0 

def list_users():
    # return the list of users present in the user database

    os.system("getent passwd | egrep  '(/bin/bash)|(/bin/zsh)|(/bin/sh)' | cut -f1 -d:")
    print("\n")

def create_user(username, uuid, group, root, set_password):
    # given an username, the function will create a new user
    # user can choose to create user as root, set password, group and specific user uuid
    # HACK: it's not possible to pass more than on group during the creation

    cmd = "useradd -d /home/{username} {username} ".format(group=group, username=username)
    if (root == "y" or root == "Y"):
        cmd += "-r "

    if uuid:
        cmd += "-u {uuid} ".format(uuid=uuid)

    group_len = len(group)
    if group_len:
        if group_len == 1:
            cmd += "-g {group} ".format(group=group)
        # else:
        #     cmd += "-G "
        #     for elem in group:
        #         cmd += "{elem},".format(elem=elem)

    if subprocess.check_output(cmd, shell=True) == 0:
        ui.print_color_msg("Operation failed", colors.COLOR_RED)
        ui.user_menu()
        return 0;
    else:
        ui.print_color_msg("User created successfully", colors.COLOR_GREEN)
        if (set_password == "y" or set_password == "Y"):
            subprocess.call("passwd " + f"{username}", shell=True)
        return 1;

# def change_password(username):


def change_username(prev_user, new_user):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename
    cmd = shlex.split("usermod")
    args = shlex.split("-l {new} {old}".format(new=new_user, old=prev_user))

    try:
        print(USERMOD + args)
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

    cmd = "USERMOD -g {main_group} {username}".format(main_group=main_group, username=username)
    return os.system(cmd) == 0

def change_home_directory(username, path, move_files):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename 
    # nemmeno sull'esistenza della directory TODO: aggiungere controllo

    cmd  = "USERMOD -d {path} {username}".format(path=path, username=username)
    if(move_files == "y"):
        cmd = "USERMOD -d {path} -m {username}".format(path=path, username=username)
    return os.system(cmd) == 0

def change_user_uid(username, uid):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename 
    # nemmeno sulla corretteza del uid

    cmd = "USERMOD -u {uid} {username}".format(uid=uid, username=username)
    return os.system(cmd) == 0

def change_user_shell(username, shell):
    # dato un username e una stringa (nuovo username) modifica l'username con la nuova stringa, non vengono fatti controlli sull'esistenza dell'usename 
    # nemmeno sull'esistenza della directory TODO: aggiungere controllo

    cmd = "USERMOD -s {shell} {username}".format(shell=shell, username=username)
    return os.system(cmd) == 0

def delete_user(username):
    # dato un username la funzione controlla l' esistenza dell'username e in caso di corretteza, elimina l'utente
    # non vengono eliminati i dati relativi all'utente
    # HACK: aggiungere la possibilit`a di eliminare i dati dell'utente (home directory)

    user = username.strip()
    if check_user_exists(user):
        os.system(f"userdel {user}")
        ui.print_color_msg(f"User {username} deleted", colors.COLOR_GREEN)
    else:
        ui.print_color_msg("Error, I can't delete the user inserted", colors.COLOR_RED)
