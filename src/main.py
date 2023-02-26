import click
from .logging.logger import setup_logger
from .utils.extractors.factory import extractor_factory

log = setup_logger('root')


@click.command()
@click.option('-o', '--origin', 'origin', default='csv')
@click.argument("filepath", type=click.Path(exists=True))
def run(origin, filepath):
    try:
        loader = extractor_factory(origin)
        loader.import_data(filepath)
    except Exception:
        return
