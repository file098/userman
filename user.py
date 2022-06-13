import os
import ui, colors

def check_user_exists(user):
    return os.system(f"id {user} &>/dev/null ") == 0   

def create_user(username, uuid, group, root, set_password):
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

    result = os.system(cmd)
    if result == 0:
        ui.print_color_msg("User created successfully", colors.COLOR_GREEN)
        if (set_password == "y" or set_password == "Y"):
            os.system(f"passwd {username}")
        return 1;
    else:
        ui.print_color_msg("Operation failed", colors.COLOR_RED)
        ui.user_menu()
        return 0;


def change_username(prev_user, new_user):
    if os.system(f"usermod -l {new_user} {prev_user}") == 0:
        ui.print_color_msg("Username changed successfully", colors.COLOR_GREEN)
    else:
        ui.error_message()


def change_home_directory(user, path, move_files):
    cmd  = "usermod -d {path} {user}".format(path=path, user=user)
    if(move_files == "y"):
        cmd = "usermod -d {path} -m {user}".format(path=path, user=user)
    return os.system(cmd) == 0

def delete_user(username):
    user = username.strip()
    if check_user_exists(user):
        os.system(f"userdel {user}")
        ui.print_color_msg(f"User {username} deleted", colors.COLOR_GREEN)
    else:
        ui.print_color_msg("Error, I can't delete the user inserted", colors.COLOR_RED)
