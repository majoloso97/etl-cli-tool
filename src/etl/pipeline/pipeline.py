import logging
from typing import List, Callable
from ..extractors.abstract_extractor import AbstractExtractor
from ..loader.loader import Loader


log = logging.getLogger('root')


class Pipeline():
    def __init__(self,
                 extractor: AbstractExtractor,
                 extraction_origin_path: str,
                 transformations: List[Callable]):
        self.extractor = extractor
        self.extraction_origin_path = extraction_origin_path
        self.transformations = transformations

    def build_log(self, logger, message):
        extra = {'feature': 'PIPELINE'}
        logger(msg=message, extra=extra)

    def extract(self):
        self.extractor.import_data(self.extraction_origin_path)
        self.data = self.extractor.valid_df

    def transform(self):
        for transformation in self.transformations:
            self.data = transformation(self.data)

    def load(self):
        loader_instance = Loader(self.data)
        loader_instance.load_data()

    def run(self):
        try:
            self.build_log(log.info, "Starting extraction process")
            self.extract()
            self.build_log(log.info, "Starting to apply defined transformations")
            self.transform()
            self.build_log(log.info, "Starting to load data to database")
            self.load()
            self.build_log(log.info, "ETL ran sucessfully")
        except Exception:
            self.build_log(log.critical, "ETL can't save data. Check previous logs for information")
