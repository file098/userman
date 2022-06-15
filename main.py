import os, sys
import ui, user, colors
import atexit

def is_root():
    # functions that checks if user ran program with root privileges
    # else it quits

    if os.geteuid() != 0:
        ui.print_color_msg("You must be root to run this program", colors.COLOR_RED)
        exit()

def main():

    is_root()
    ui.clear()
    ui.main_menu()

main()