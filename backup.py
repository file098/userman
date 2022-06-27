import os, datetime, subprocess, shlex
import ui, colors, user

def backup_user(username, exclude_list=[], backup_path="/home", compress=False):


    # default saving backup path
    if backup_path == "":
        if os.path.exists("/backup"):
            backup_path = "/backup"
        else:
            # creates a backup directory if it doesn't exist inside home
            home_dir = "/home"
            path = os.path.join(home_dir, "backup")
            if not os.path.exists(path):
                os.mkdir(path)
            backup_path = path

    # check if folder and user exits otherwise stops
    if user.check_user_exists(username):

        args = shlex.split("-av /home/{username} {backup_path}".format(username=username, backup_path=backup_path))
        
        # turn on compression 
        if compress: args += ["-z"] 
        # adds to the arguments all the listed excluded folders, if there are any
        if len(exclude_list) >= 0:
            for folders in exclude_list:
                args.append("--exclude=" + folders)
        # Tries to run command, if it fails then it will print the error message
        try:
            response = subprocess.check_call(["rsync"] + args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            ui.print_color_msg("backup_user failed with the following error:", colors.COLOR_RED)
            response = err.returncode
            print(response)
        else:
            ui.print_color_msg("Operation successfully completed", colors.COLOR_GREEN)
            return True
    else:
        ui.error_message()
        return False