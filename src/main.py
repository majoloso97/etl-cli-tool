import click
from .logging.logger import setup_logger
from .core.config import (get_global_settings,
                          read_db_settings_from_env,
                          read_db_settings_from_input)
from .etl.pipeline.worker import run_pipeline

# CLI options for setting log output and database auth method
config_log_options = {'C': 'Console', 'L': 'Logfile', 'D': 'Database'}
config_db_options = {'E': 'Environment variables', 'P': 'User Prompt'}

# Help text for CLI
log_help = '''Controls the output of logs. Choose from either
console [C], logfile [L], or database [D]. Defaults to [C] for
just showing logs in terminal. [L] and [D] show terminal logs too
but also store logs in either a .log file in the directory where
the ETL is run or a table in the same database the data is stored.'''
db_help = '''Controls the way the authentication to the db will
be managed. Choose from either environment [E] or prompts [P].
[E] will try to load database credentials for environment
of logs. Defaults to [C] for just showing logs in terminal. [L]
and [D] store logs in either a .log file in the directory where
the ETL is run or a table in the same database the data is stored.'''

# Load (or create) current global settings
settings = get_global_settings()
init_log_type = settings['LOG_TYPE']
init_db_auth = settings['DB_AUTH']

# Set up logger with current configuration
log = setup_logger('root', init_log_type)


# Define RUN command
@click.command()
@click.option('-o', '--origin', 'origin', default='csv',
              help='Set data source type. Only CSV is currently available.')
@click.argument("filepath", type=click.Path(exists=True))
def run(origin, filepath):
    '''
    Run ETL pipeline on the specified FILEPATH.

    FILEPATH = Path to the file to be used to pull data from. Must match --origin type.
    '''
    run_pipeline(origin_type=origin,
                 origin_path=filepath)


# Define CONFIG command
@click.command()
@click.option('--log-type', 'log_type', default=init_log_type,
              type=click.Choice(config_log_options.keys(),
                                case_sensitive=False),
              help=log_help)
@click.option('--db-auth', 'db_auth', default=init_db_auth,
              type=click.Choice(config_db_options.keys(),
                                case_sensitive=False),
              help=db_help)
def config(log_type, db_auth):
    '''Change log-type and db-auth settings for the ETL CLI tool'''
    log.info(f'Log type set to {config_log_options[log_type]} [{log_type}].',
             extra={'feature': 'CLI CONFIG'})
    log.info(f'Db Auth set to {config_db_options[db_auth]} [{db_auth}].',
             extra={'feature': 'CLI CONFIG'})
    if db_auth == 'E':
        read_db_settings_from_env(log_type, db_auth)
    read_db_settings_from_input(log_type, db_auth)


# Define SHOW command
@click.command()
def show():
    '''Shows current configuration for the ETL CLI tool'''
    log.info(f'Current log-type set to {init_log_type}',
             extra={'feature': 'CLI SHOW'})
    log.info(f'Current db-auth set to {init_db_auth}',
             extra={'feature': 'CLI SHOW'})
