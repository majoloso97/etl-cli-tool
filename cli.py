import click
from src.main import run, config, show

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(run)
cli.add_command(config)
cli.add_command(show)
