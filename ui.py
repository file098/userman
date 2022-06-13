import os, re
import user

def main_menu():
    main_menu = ["User management", "Folders management", "Backups", "Quit"]
    print_choises(main_menu)
    choice = what_to_do()
    valid = False
    while(not valid):
        match choice:
            case "0":
                user_menu()
                valid = True
            case "1":
                print("Folders")
                valid = True
            case "2":
                print("Backups")
            case "3":
                exit()
            case _:
                print("Error")


def user_menu():
    user_choices = ["Create user", "Delete user","Show users","" "Quit"]
    print_choises(user_choices)
    choice = what_to_do()
    valid = False
    while(not valid):
        match choice:
            case "0":
                username = input("Username for the new user\n")
                uuid = input("User UUID for the new user, blank if default\n")
                group = input("Group for the new user\n")
                system = input("Root user? (y/n)\n").lower()
                passwd = input("Do you want to set a password for the new user? (y/n)\n").lower()
                user.create_user(username, uuid, group, system, passwd)
                valid = True
            case "1":
                list_users()
                username = input("Which user do you want to delete?\n")
                valid = True
                user.delete_user(username)

            case "2":
                list_users()
                valid = True
            case _:
                print("Error")
    main_menu()

def list_users():
    os.system("getent passwd | egrep  '(/bin/bash)|(/bin/zsh)|(/bin/sh)' | cut -f1 -d:")
    print("\n")

def print_choises(choices):
    for i in range(len(choices)):
        os.system("tput setaf 2")
        print(""+ str(i) + "\t" + choices[i])
        os.system("tput setaf 7")


def what_to_do():
    return input('What should I do?\n')