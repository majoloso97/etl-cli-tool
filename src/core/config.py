import os
import json
import getpass

CONFIG_PATH = os.path.expanduser('~/.etl/')
CONFIG_FILE = 'settings.json'


def write_settings(settings):
    with open(f'{CONFIG_PATH}{CONFIG_FILE}', 'w') as configfile:
        configfile.write(settings)


def read_settings():
    with open(f'{CONFIG_PATH}{CONFIG_FILE}', 'r') as configfile:
        return json.load(configfile)


def get_global_settings():
    try:
        # Read settings from .json file
        settings = read_settings()
        if len(settings.keys()) == 0:
            raise RuntimeError('No available settings')

    except Exception:
        # Create .ini file with default values if it doesn't exist
        settings = {}
        settings['LOG_TYPE'] = 'C'
        settings['DB_AUTH'] = 'P'
        settings['DB_HOST'] = '127.0.0.1'
        settings['DB_PORT'] = '3306'
        settings['DB_USER'] = 'user'
        settings['DB_PASS'] = 'admin'
        settings['DB_NAME'] = 'etl_db'

        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        write_settings(json.dumps(settings))

    return settings


def set_global_settings(**kwargs):
    settings = get_global_settings()

    for key in kwargs.keys():
        settings[key] = kwargs[key]

    write_settings(json.dumps(settings))
    return settings


def read_db_settings_from_env():
    db_host = os.getenv(['DB_HOST'], '127.0.0.1')
    db_port = os.getenv(['DB_PORT'], '3306')
    db_user = os.getenv(['DB_USER'], 'user')
    db_pass = os.getenv(['DB_PASS'], 'admin')
    db_name = os.getenv(['DB_NAME'], 'etl_db')
    set_global_settings(DB_HOST=db_host,
                        DB_PORT=db_port,
                        DB_USER=db_user,
                        DB_PASS=db_pass,
                        DB_NAME=db_name)


def read_db_settings_from_input():
    curr = get_global_settings()
    host = input(f'Database Host (or Enter to use {curr["DB_HOST"]}): ')
    port = input(f'Database Port (or Enter to use {curr["DB_PORT"]}): ')
    user = input(f'Database Username (or Enter to use {curr["DB_USER"]}): ')
    passwrd = getpass.getpass(f'Database Password (or Enter to use existing): ')
    name = input(f'Database Name (or Enter to use {curr["DB_NAME"]}): ')

    db_host = host if host else curr['DB_HOST']
    db_port = port if port else curr['DB_PORT']
    db_user = user if user else curr['DB_USER']
    db_pass = passwrd if passwrd else curr['DB_PASS']
    db_name = name if name else curr['DB_NAME']

    set_global_settings(DB_HOST=db_host,
                        DB_PORT=db_port,
                        DB_USER=db_user,
                        DB_PASS=db_pass,
                        DB_NAME=db_name)
