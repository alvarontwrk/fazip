#!/home/alvaro/.miniconda3/envs/fazip/bin/python

from fazip import fazip
import sys
import getpass


def do_extraction(zipname):
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    fazip.unzip_files(db, zipname)
    db.close()


def do_compression(zipname, files):
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    str_files = " ".join(files)
    fazip.zip_files(db, zipname, str_files)
    db.close()


def do_add_user(database):
    print("\nEnter the new user's name")
    user = input("[fazip]> ")
    if fazip.add_user_db(database, user):
        print("User successfully registered!")
    else:
        print("User already registered :(")


def do_edit_user(database):
    print("\nEnter the user's name you want to edit")
    user = input("[fazip]> ")
    if fazip.modify_user_db(database, user):
        print("User successfully edited!")
    else:
        print("User doesn't exists :(")


def do_remove_user(database):
    print("\nEnter the user's name you want to remove")
    user = input("[fazip]> ")
    if fazip.remove_user_db(database, user):
        print("User successfully removed!")
    else:
        print("User doesn't exists :(")


def do_list_users(database):
    users = fazip.get_users_db(database)
    if users:
        print("\nThose are the registered users:")
        for user in users:
            print("=> {}".format(user))
    else:
        print("There are no users registered :(")


def do_change_pass(database):
    print("WARNING: You will not be able to extract files" +
          "from previously created zip files")
    verify = input("Proceed (y/[n])? ")
    if verify == 'y' or verify == 'yes':
        oldp = getpass.getpass("Enter your actual password: ")
        if fazip.get_password_zip(database) == oldp:
            first = getpass.getpass("Enter your new password: ")
            second = getpass.getpass("Enter your new password again: ")
            if first == second:
                fazip.set_password_zip(database, first)
                print("\nPassword changed successfully!")
                print("Please log in again")
                sys.exit()
            else:
                print("Those passwords didn't match.")
        else:
            print("Access denied")
            sys.exit()


def print_menu(options):
    print(" ====================================")
    print("|| \t   CONFIGURATION MENU\t    ||")
    print(" ====================================")
    print("\t-> {}) Exit".format(options['exit_menu']))
    print("\t-> {}) List users".format(options['list_users']))
    print("\t-> {}) Add user".format(options['add_user']))
    print("\t-> {}) Edit user".format(options['edit_user']))
    print("\t-> {}) Remove user".format(options['remove_user']))
    print("\t-> {}) Change password (CRITICAL)".format(options['change_pass']))


def menu(options, selection):
    pass


def do_configuration(login=False):
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    options = {'exit_menu': 0, 'list_users': 1, 'add_user': 2,
               'edit_user': 3, 'remove_user': 4, 'change_pass': 5}
    if not login:
        pwd = getpass.getpass("Enter password: ")
        if not fazip.get_password_zip(db) == pwd:
            print("Access denied")
            sys.exit()

        print_menu(options)

    try:
        selection = int(input("\n[fazip]> "))
    except Exception:
        selection = -1
        print("Seriously? That's not a number -.-")

    if options['exit_menu'] <= selection <= options['change_pass']:
        if selection == options['add_user']:
            do_add_user(db)

        elif selection == options['edit_user']:
            do_edit_user(db)

        elif selection == options['remove_user']:
            do_remove_user(db)

        elif selection == options['list_users']:
            do_list_users(db)

        elif selection == options['exit_menu']:
            sys.exit()

        elif selection == options['change_pass']:
            do_change_pass()

        db.close()

    else:
        print("Wrong answer")

    do_configuration(True)


def print_help():
    print("It looks like you missed something :(")
    print("\tFormat: fazip x <zipfile>")
    print("\tFormat: fazip a <zipfile> <files>")


def main():
    if 2 < len(sys.argv) == 3 and sys.argv[1] == 'x':
        do_extraction(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'a':
        do_compression(sys.argv[2], sys.argv[3:])
    elif len(sys.argv) == 2 and sys.argv[1] == 'config':
        print(fazip.utils.HEADER)
        do_configuration()
    else:
        print_help()


if __name__ == '__main__':
    main()
