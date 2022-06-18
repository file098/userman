import os, sys, subprocess, shlex
import ui, user, colors
import atexit

def is_root():
    # functions that checks if user ran program with root privileges
    # else it quits

    if os.geteuid() != 0:
        sys.exit("You must be root to run this program")

def main():

    is_root()
    ui.clear()
    ui.main_menu()

main()