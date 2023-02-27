import logging
from typing import List, Callable
from ..extractors.abstract_extractor import AbstractExtractor

log = logging.getLogger('root')


class Pipeline():
    def __init__(self,
                 extractor: AbstractExtractor,
                 loader,
                 *args: List[Callable]):
        self.extractor = extractor
        self.transformations = [args]
        self.loader = loader

    def log(self, level, message):
        extra = {'feature': 'PIPELINE MANAGER'}
        log.log(level=level, msg=message, extra=extra)

    def extract(self):
        pass

    def transform(self):
        pass

    def load(self):
        pass

    def run(self):
        self.log(logging.INFO, "Starting extraction process")
        self.extract()
        self.log(logging.INFO, "Starting to apply defined transformations")
        self.transform()
        self.log(logging.INFO, "Starting to load data to database")
        self.load()
        self.log(logging.INFO, "ETL ran sucessfully")
