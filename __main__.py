from fazip import connect_to_db, unzip_files, zip_files, get_mysql_info
from fazip import add_user_db, modify_user_db, remove_user_db, get_users_db
from fazip import get_password_zip, set_password_zip
import sys
import getpass


def do_extraction(zipname):
    host, user, pwd = get_mysql_info()
    db = connect_to_db(user, pwd, host)
    unzip_files(db, zipname)
    db.close()


def do_compression(zipname, files):
    host, user, pwd = get_mysql_info()
    db = connect_to_db(user, pwd, host)
    str_files = " ".join(files)
    zip_files(db, zipname, str_files)
    db.close()


def do_configuration(login=False):
    host, user, pwd = get_mysql_info()
    db = connect_to_db(user, pwd, host)
    if not login:
        pwd = getpass.getpass("Enter password: ")
        if not get_password_zip(db) == pwd:
            print("Access denied")
            sys.exit()
    exit_menu = 0
    list_users = 1
    add_user = 2
    edit_user = 3
    remove_user = 4
    change_pass = 5
    # print("Well... choose what do you want to do.")
    if not login:
        print(" ====================================")
        print("|| \t   CONFIGURATION MENU\t    ||")
        print(" ====================================")
        print("\t-> {}) Exit".format(exit_menu))
        print("\t-> {}) List users".format(list_users))
        print("\t-> {}) Add user".format(add_user))
        print("\t-> {}) Edit user".format(edit_user))
        print("\t-> {}) Remove user".format(remove_user))
        print("\t-> {}) Change password (CRITICAL)".format(change_pass))
        print()

    try:
        selection = int(input("[fazip]> "))
    except Exception:
        selection = -1
        print("Seriously? That's not a number -.-")

    if exit_menu <= selection <= change_pass:
        if selection == add_user:
            print("\nEnter the new user's name")
            user = input("[fazip]> ")
            if add_user_db(db, user):
                print("User successfully registered!")
            else:
                print("User already registered :(")

        elif selection == edit_user:
            print("\nEnter the user's name you want to edit")
            user = input("[fazip]> ")
            if modify_user_db(db, user):
                print("User successfully edited!")
            else:
                print("User doesn't exists :(")

        elif selection == remove_user:
            print("\nEnter the user's name you want to remove")
            user = input("[fazip]> ")
            if remove_user_db(db, user):
                print("User successfully removed!")
            else:
                print("User doesn't exists :(")

        elif selection == list_users:
            users = get_users_db(db)
            if users:
                print("\nThose are the registered users:")
                for user in users:
                    print("=> {}".format(user))
            else:
                print("There are no users registered :(")

        elif selection == exit_menu:
            sys.exit()

        elif selection == change_pass:
            print("WARNING: If you change your password, you will not be\
                  able to extract files from previously created zip files")
            verify = input("Proceed (y/[n])? ")
            if verify == 'y' or verify == 'yes':
                oldp = getpass.getpass("Enter your actual password: ")
                if get_password_zip(db) == oldp:
                    first = getpass.getpass("Enter your new password: ")
                    second = getpass.getpass("Enter your new password again: ")
                    if first == second:
                        set_password_zip(db, first)
                        print("\nPassword changed successfully!")
                        print("Please log in again")
                        sys.exit()
                    else:
                        print("Those passwords didn't match.")
                else:
                    print("Access denied")
                    sys.exit()

        db.close()

    else:
        print("Wrong answer")

    do_configuration(True)


def print_help():
    print("It looks like you missed something :(")
    print("\tFormat: fazip x <zipfile>")
    print("\tFormat: fazip a <zipfile> <files>")


if __name__ == '__main__':
    header = chr(27) + "[2J" + """
\t    ____            _
\t   / __/___ _____  (_)___
\t  / /_/ __ `/_  / / / __ \\
\t / __/ /_/ / / /_/ / /_/ /
\t/_/  \__,_/ /___/_/ .___/
                 /_/
"""
    print(header)
    if 2 < len(sys.argv) == 3 and sys.argv[1] == 'x':
        do_extraction(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'a':
        do_compression(sys.argv[2], sys.argv[3:])
    elif len(sys.argv) == 2 and sys.argv[1] == 'config':
        do_configuration()
    else:
        print_help()
