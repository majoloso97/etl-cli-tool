import click
from src.main import hello_world

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
def hello():
    '''Test functionality of CLI setup'''
    hello_world()
