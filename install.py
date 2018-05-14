import configparser
import getpass
import pathlib
from fazip import fazip
import os
import sys


def write_config():
    print('\n[fazip] MySQL configuration:')
    host = input("[fazip] => Host (default=localhost): ")
    user = input("[fazip] => User (default=root): ")
    pwd = getpass.getpass("[fazip] => Password: ")

    if not host:
        host = 'localhost'
        if not user:
            user = 'root'

    config = configparser.ConfigParser()
    config['mysql'] = {'host': host, 'user': user, 'password': pwd}

    config_path = pathlib.Path(fazip.utils.CONFIG_PATH)
    config_path.mkdir(exist_ok=True)

    with open(fazip.utils.CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    print("[fazip] Done!")


def set_master_pass():
    print("[fazip] Setting password...")
    first = getpass.getpass("[fazip] Enter your master password: ")
    second = getpass.getpass("[fazip] Enter your master password again: ")
    if first == second:
        return first
    else:
        print("[fazip] Error: Those passwords didn't match.")
        set_master_pass()
    print("[fazip] Done!")


def write_db():
    print("\n[fazip] Creating the database...")
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    fazip.remove_db(db)
    fazip.create_db(db)
    fazip.create_table_db(db)
    master = set_master_pass()
    fazip.set_password_zip(db, master)
    print("[fazip] Done!")


def create_symlink():
    print("\n[fazip] Creating symbolic link...")
    try:
        os.symlink(fazip.utils.MAIN_PATH, fazip.utils.BIN_PATH)
    except Exception as e:
        error_string = str(e)
        if 'denied' in error_string:
            print("[fazip] Error: You need root permissions.")
            sys.exit()
        else:
            os.remove(fazip.utils.BIN_PATH)
            os.symlink(fazip.utils.MAIN_PATH, fazip.utils.BIN_PATH)
    print("[fazip] Done!")


def exists_fazip_db():
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    return fazip.exists_db(db)


def knows_old_password():
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    pwd = getpass.getpass("[fazip] Enter your old master pass: ")
    return pwd == fazip.get_password_zip(db)


def main():
    print(fazip.utils.HEADER)
    try:
        f = open(fazip.utils.CONFIG_FILE, 'r')
        f.close
        print('[fazip] WARNING: This will overwrite the saved MySQL' +
              'login credentials')
        verify = input("[fazip] Proceed (y/[n])? ")
    except Exception:
        verify = 'y'

    if verify == 'y':
        create_symlink()
        write_config()
        fail = False
        if exists_fazip_db():
            print("\n[fazip] Database detected.")
            verify = input("[fazip] Overwrite it (y/[n])? ")
            if verify == 'y' and knows_old_password():
                write_db()
            else:
                print("\n[fazip] Access denied")
                fail = True
        else:
            write_db()

        if not fail:
            print('\n[fazip] Installation successfully completed!')


if __name__ == '__main__':
    main()
