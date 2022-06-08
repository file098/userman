import os, sys
import ui



def main():
    print('''
    Welcome to UserMan
    ''')
    choices = ["User management", "Folders management", "Backups"]
    ui.print_choises(choices)
    choise = input("What should I do?\n")

    if(choise == "0"):
        print("1");
    elif(choise == "1"):
        print("2");
    elif(choise == "2"):
        print("3");
    else:
        print("wrong choice");
        
main()