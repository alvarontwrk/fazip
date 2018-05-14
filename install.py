import os
import inspect
import configparser
import getpass
import pathlib
from fazip import fazip


def write_config():
    host = input("=>Host: (default=localhost)")
    user = input("=>User: (default=root)")
    pwd = getpass.getpass("=>Password: ")

    if not host:
        host = 'localhost'
    if not user:
        user = 'root'

    config = configparser.ConfigParser()
    config['mysql'] = {'host': host, 'user': user, 'password': pwd}

    project_path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    config_path = pathlib.Path('{}/config'.format(project_path))
    config_path.mkdir(exist_ok=True)
    configfile_path = '{}/config.ini'.format(config_path)

    with open(configfile_path, 'w') as configfile:
        config.write(configfile)


def set_master_pass():
    first = getpass.getpass("Enter your master password: ")
    second = getpass.getpass("Enter your master password again: ")
    if first == second:
        return first
    else:
        print("Those passwords didn't match.")
        set_master_pass()


def write_db():
    host, user, pwd = fazip.get_mysql_info()
    db = fazip.connect_to_db(user, pwd, host)
    fazip.remove_db(db)
    fazip.create_db(db)
    fazip.create_table_db(db)
    master = set_master_pass()
    fazip.set_password_zip(db, master)


def main():
    print('WARNING: This action will kill the previous installation if exists')
    verify = input("Proceed (y/[n])? ")
    if verify == 'y' or verify == 'yes':
        print('\nMySQL configuration:')
        write_config()
        write_db()


if __name__ == '__main__':
    main()
