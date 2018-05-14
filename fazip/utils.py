import os
import inspect


PATH = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))[:-6]
CONFIG_PATH = '{}/config'.format(PATH)
CONFIG_FILE = '{}/config.ini'.format(CONFIG_PATH)
HEADER = chr(27) + "[2J" + """
\t    ____            _
\t   / __/___ _____  (_)___
\t  / /_/ __ `/_  / / / __ \\
\t / __/ /_/ / / /_/ / /_/ /
\t/_/  \__,_/ /___/_/ .___/
\t                 /_/
"""
BIN_PATH = '/usr/local/bin/fazip'
MAIN_PATH = '{}/main.py'.format(PATH)


if __name__ == '__main__':
    print(HEADER)
    print(PATH)
    print(CONFIG_PATH)
    print(CONFIG_FILE)
    print(BIN_PATH)
    print(MAIN_PATH)
