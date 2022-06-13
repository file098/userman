import os 

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
        print(f"Operation successful, created user {username}")
        if (set_password == "y" or set_password == "Y"):
            os.system(f"passwd {username}")
        return 1;
    else:
        print("Operation failed")
        return 0;


def update_user(username):
    print("Update user")

def delete_user(username):
    user = username.strip()
    if os.system(f"id {user} &>/dev/null ") == 0:
        os.system(f"userdel {user}")
    else:
        print("Error, I can't delete the user inserted")
