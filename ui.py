import os

def print_choises(choices):
    for i in range(len(choices)):
        os.system("tput setaf 2")
        print(""+ str(i) + "\t" + choices[i])
        os.system("tput setaf 7")


def user_management_choises():
    print('''
    
    ''')

def what_to_do():
    print('What should I do?\n')