import os
import json

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
        settings['DB_PASS'] = 'root'
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
