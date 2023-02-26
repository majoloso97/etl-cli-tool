import logging
from .csv_extractor import CsvExtractor

log = logging.getLogger('root')


def extractor_factory(loader_type: str):
    factories = {
        'csv': CsvExtractor()
    }

    if loader_type not in factories:
        log.error('Loader not available', extra={'feature': 'EXTRACT'})
        raise NotImplementedError('Loader not available. Cannot proceed.')

    return factories[loader_type]
