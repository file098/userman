
setps3() {
    PS3="$1 (press enter for choices)>"
}
setmainprompt() {
    setps3 "Main menu"
}
setaddprompt() {
    setps3 "ADD USER menu"
}

pressenter() {
    read -p "Press enter to continue:" _tmp
}
derr() {
    echo 1>&2 ${CMDNAME} ERROR: $*
    return 1
}
msg() {
    echo ${CMDNAME} NOTICE: $*3
    return 0
}

badchoice() {
    err "Bad choice!";
    return 1
}

do_add_one_user() {
    _name="$1"
    _pass="$2"

    # useradd -u ABCDE -g users -d /home/username -s /bin/bash -p $(echo mypasswd | openssl passwd -1 -stdin) username
    # -u userid
    # -d groupname
    # -d user home directory
    # -s default shell
    # -p password
    # Openssl passwd will generate hash of mypasswd to be used as secure password.

    tput setaf 1
    if [ ${#_pass} -ne 0 ]; then
        echo "Password set"
        # check if system has adduser and if so use that to create user with passwd, otherwise use useradd
        # useradd -u ABCDE -g users -d /home/${_name} -s /bin/bash -p $(echo mypasswd | openssl passwd -1 -stdin) {_name}
    else 
        echo "User will have to set their own password (passwd on first login)"
    fi
    tput setaf 7
    pressenter
}

do_manual_add() {
    read -p "Username:" _username
    read -p "Passowrd:" _password
    echo
    do_add_one_user "${_username}" "${_password}"
}

do_txt_add() {
    read -p "Filename:" _filename
    [[ -z "${_filename}" ]] && return
    echo "add code here for adding users from ${_filename}"
    echo "The code should call do_add_one_user function for every line"
    pressenter
}

do_adduser() {
    setaddprompt
    _arr_add=("Add manually" "Add via TXT" "return to main menu" "exit program")
    select add_action in "${_arr_add[@]}"
    do
        case "$REPLY" in
            1) do_manual_add ;;
            2) do_txt_add ;;
            3) return ;;
            4) exit 0 ;;
            *) badchoice ;;
        esac
        setaddprompt
    done
}

do_deleteuser() {
    echo "enter code for deleting user here"
    pressenter
}

uidcheck() {
    owner=${owner:-$(/usr/bin/id -u)}
    if [ "$owner" != "0" ]; then
        err 'Must be root'
        exit 1
    fi
}

## MAIN PROGRAM

CMDNAME=$(basename $0)
#uidcheck   #uncomment when need

_user_manager() {
    setaddprompt
    _arr_man=("Add manually" "Add via TXT" "return to main menu" "exit program")
    select man_action in "${_arr_man[@]}"
    do
        case "$REPLY" in
            1) do_adduser ;;
            2) do_deleteuser ;;
            3) return ;;
            4) exit 0 ;;
            *) badchoice ;;
        esac
        setaddprompt
    done
}

#_arr_main=("Add user" "Delete user" "Exit program")
_arr_main=("User managment" "Exit program")
setmainprompt
select main_action in "${_arr_main[@]}"
do
    case "$REPLY" in
        1) do_adduser ;;
        2) do_deleteuser  ;;
        3) exit 0 ;;
        *) badchoice ;;
    esac
    setmainprompt
done
