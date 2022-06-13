import os, re
import user, colors


def main_menu():
    main_title()
    main_menu_choices = ["User management", "Folders management", "Backups", "Quit"]
    print_choices(main_menu_choices)
    choice = what_to_do()
    valid = False
    while(not valid):
        match choice:
            case "1":
                user_menu()
                valid = True
            case "2":
                print("Folders")
                valid = True
            case "3":
                print("Backups")
                valid = True
            case "q":
                exit()
            case _:
                print_color_msg("Invalid option", colors.COLOR_RED)
                main_menu()


def user_menu():
    user_choices = ["Create user", "Delete user","Show users", "Update users", "Back"]
    print_choices(user_choices)
    choice = what_to_do()
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
                list_users()
                username = input("Which user do you want to delete?\n")
                valid = True
                user.delete_user(username)
            case "3":
                list_users()
                valid = True
                user_menu()
            case "4":
                update_user()
                
            case "b":
                valid = True
            case _:
                print_color_msg("Invalid option", colors.COLOR_RED)
                main_menu()

    # clear()
    main_menu()

def update_user():
    print("Which user do you want to update?\n")
    list_users()
    username = input("\n").strip()
    if user.check_user_exists(username):
        update_choices = ["Change username", "Change home directory", "Change user's UID", "Add group to user", "Back", "Main menu"]
        print_choices(update_choices)
        choice = what_to_do()

        valid = False
        while(not valid):
            match choice:
                case "1":
                    new_user = input(f"Insert new username for {username}\n").strip()
                    user.change_username(username, new_user)
                    valid = True
                case "2":
                    move_files = input("Move all files to new directory? (y/n)\n").lower().strip()
                    destination = input("Insert the destination directory: ")
                    valid = user.change_home_directory(username, destination, move_files)
                    
                case "3":
                    list_users()
                    valid = True
                case "b":
                    valid = True
                    update_user()
                case "q":
                    main_menu()
                case _:
                    print("Invalid option\n")
                    valid = True
    else:
        print_color_msg("Invalid username", colors.COLOR_RED)
        update_user()

    main_menu()


def list_users():
    os.system("getent passwd | egrep  '(/bin/bash)|(/bin/zsh)|(/bin/sh)' | cut -f1 -d:")
    print("\n")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_choices(choices):
    for i in range(len(choices)):
        os.system("tput setaf 6")
        match choices[i]:
            case "Quit" | "Main menu":
                print("q" + "\t" + choices[i])
            case "Back":
                print("b" + "\t" + choices[i])
            case _:
                print(""+ str(i+1) + "\t" + choices[i])
        os.system("tput setaf 7")
    print("\n")

def print_color_msg(msg, color):
    os.system(f"tput setaf {color}")
    print(msg + "\n")
    os.system("tput setaf 7")


def error_message():
    print("Error")

def what_to_do():
    return input('What should I do?\n')

def main_title():
    print_color_msg('''
    Welcome to UserMan
    ''', colors.COLOR_BLUE)