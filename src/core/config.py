import os
import configparser

CONFIG_PATH = os.path.expanduser('~/.etl/')
CONFIG_FILE = 'config.ini'


def write_settings(config):
    with open(f'{CONFIG_PATH}{CONFIG_FILE}', 'w') as configfile:
        config.write(configfile)


def get_global_settings():
    try:
        # Read config from .ini file
        config = configparser.ConfigParser()
        config.read(f'{CONFIG_PATH}{CONFIG_FILE}')
        if len(config.sections()) == 0:
            raise RuntimeError('No available settings')

    except Exception:
        # Create .ini file with default values if it doesn't exist
        config = configparser.ConfigParser()
        config['DEFAULT']['LOG_TYPE'] = 'C'
        config['DEFAULT']['DB_AUTH'] = 'P'
        config['DEFAULT']['DB_HOST'] = '127.0.0.1'
        config['DEFAULT']['DB_PORT'] = '3306'
        config['DEFAULT']['DB_USER'] = 'user'
        config['DEFAULT']['DB_PASS'] = 'root'
        config['DEFAULT']['DB_NAME'] = 'etl_db'

        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        write_settings(config)

    return config['DEFAULT']


def set_global_settings(**kwargs):
    settings = get_global_settings()
    config = configparser.ConfigParser()

    for key in kwargs.keys():
        if key in settings.keys():
            config['DEFAULT'][key] = kwargs[key]

        config['DEFAULT'][key] = settings[key]

    write_settings(config)
