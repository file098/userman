import os, re, atexit, ast, sys
import user, colors, backup

def main_menu():
    main_title()
    choice = handle_menu(["User management", "Backups", "Quit"])
    valid = False
    while(not valid):
        match choice:
            case "1":
                user_menu()
                valid = True
            case "2":
                backup_menu()
                valid = True
            case "q":
                sys.exit("Goodbye!")
            case _:
                clear()
                print_color_msg("Invalid option", colors.COLOR_RED)
                main_menu()


def user_menu():
    choice = handle_menu(["Create user", "Delete user","Show users", "Update users", "Back"])
    valid = False
    while(not valid):
        match choice:
            case "1":
                username = input("Username for the new user\n")
                uuid = input("User UUID for the new user, blank if default\n")
                group = input("Group for the new user\n")
                system = input("Root user? (y/n)\n").lower()
                passwd = input("Do you want to set a password for the new user? (y/n)\n").lower()
                user.create_user(username, uuid, group, system, passwd)
                valid = True
            case "2":
                user.list_users()
                username = input("Which user do you want to delete?\n")
                delete_home = input("Do you want to delete the user's home directory? (y/n)\n").lower().strip() == "y"
                valid = user.delete_user(username, delete_home) == 0
            case "3":
                user.list_users()
                valid = True
                user_menu()
            case "4":
                update_user()
                valid = True
            case "b":
                valid = True
                main_menu()
            case _:
                print_color_msg("Invalid option", colors.COLOR_RED)
                main_menu()
    user_menu()

def update_user():
    print("Which user do you want to update?\n")
    user.list_usernames()
    username = input("\n").strip()
    if username != "" and user.check_user_exists(username):
        choice = handle_menu(["Change username", "Change home directory", "Change user's UID", "Add group to user", "Change user's shell", "Back", "Main menu"])
        valid = False
        while(not valid):
            match choice:
                case "1":
                    new_user = input(f"Insert new username for {username}\n").strip()
                    user.change_username(username, new_user)
                    valid = True
                case "2":
                    move_files = input("Move all files to new directory? (y/n)\n").lower().strip() == "y"
                    destination = input("Insert the destination directory: ")
                    user.change_home_directory(username, destination, move_files)
                    valid = True
                case "3":
                    uid = input("Enter UID:")
                    valid = user.change_user_uid(username, shell)
                case "4":
                    group = input("Insert the group you want to add: ")
                    valid = user.change_user_main_group(username, group)
                case "5":
                    valid = user.change_user_shell(username, shell)
                case "b":
                    valid = True
                    update_user()
                case "q":
                    main_menu()
                case _:
                    # clear()
                    print("Invalid option\n")
                    valid = True
    else:
        print_color_msg("Invalid username", colors.COLOR_RED)
        update_user()
    main_menu()

def backup_menu():
    choice = handle_menu(["Backup User Home", "Back"])
    valid = False
    while(not valid):
        match choice:
            case "1":
                user.list_usernames()
                exists = False
                while not exists:
                    username = input("Which user to backup?\n")
                    
                    # check if user exists,if it doesnt then user has to repeat input, else function is called 
                    exists = user.check_user_exists(username)
                    if exists:

                        # prompt user to enter backup save path
                        backup_path = input("Where do you want to save the backup? (if not speciefied it will be saved in /home)\n").strip()
                        # list parameter can be void or a list of paths
                        exclude = input("Do you want to exclude some folders? (y/n)\n").lower().strip() == "y"
                        compress = input("Do you want to compress the backup? (y/n)\n").lower().strip() == "y"
                        stop_excluded_folders = False
                        if exclude:
                            folders = []
                            print('Please enter "done" to stop adding folders')
                            while not stop_excluded_folders:
                                # the loop keeps on getting input from user until it enconters the string "done"

                                folder = input("Please write the path of the excluded folder: ")
                                if( folder == "done" ):
                                    stop_excluded_folders = True
                                else:
                                    folders.append(folder)

                            # once it's done it calls the backup function
                            backup.backup_user(username, folders, backup_path, compress)
                        else:
                            # function without folder exclusion
                            backup.backup_user(username, [], backup_path, compress)
                            main_menu()
                    else:
                        print_color_msg("User does not exist", colors.COLOR_RED)  
                valid =  True
            case "b":
                valid = True
                clear()
                main_menu()
                
            case _:
                print("Invalid option\n")
                backup_menu()



def handle_menu(choices):
    print_choices(choices)
    return what_to_do() 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_users(usersArray):
    count = 0
    for users in usersArray:
        count += 1
        counter = "* " + str(count)
        username = " USERNAME: " + users.username
        name = " FULL NAME: " + users.name 
        uid = " UID: " + users.uid 
        id = " ID: " + users.id
        home = " HOME DIRECTORY: " + users.home_folder
        shell = " SHELL: " + users.shell
        print(counter + username + name + uid + id + home + shell)

def print_choices(choices):
    # function that takes a list of choices 
    # it prints the list with the list index starting from 1
    # handles quit e back cases

    for i in range(len(choices)):
        os.system("tput setaf 6")
        match choices[i]:
            case "Quit" | "Main menu":
                print("\t" + "q" + "\t" + choices[i])
            case "Back":
                print("\t" + "b" + "\t" + choices[i])
            case _:
                print("\t" + str(i+1) + "\t" + choices[i])
        os.system("tput setaf 7")
    print("\n")

def print_color_msg(msg, color):
    # given a string and a color taken from the CONSTANTS file, the function will print the message with the specified color and then return to regular color
    
    os.system(f"tput setaf {color}")
    print(msg + "\n")
    os.system("tput setaf 7")


def error_message():
    # simple error message
    print("Error")

def what_to_do():
    # function to get an input form the user 
    # also handles soft quit

    user_input = input('What should I do?\n\n')
    print("\n")
    return user_input

def main_title():
    # welocome title

    print_color_msg('''
    Welcome to UserMan
    ''', colors.COLOR_BLUE)