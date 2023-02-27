import click
from .logging.logger import setup_logger
from .etl.extractors.factory import extractor_factory

log = setup_logger('root')

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
    try:
        loader = extractor_factory(origin)
        loader.import_data(filepath)
    except Exception:
        return
