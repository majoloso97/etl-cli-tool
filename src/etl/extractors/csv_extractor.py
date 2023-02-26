import logging
import pandas as pd
from .abstract_extractor import AbstractExtractor

log = logging.getLogger('root')


class CsvExtractor(AbstractExtractor):
    def import_data(self, filename):
        self.verify_origin(filename)
        self.build_log(log.info, 'extracting', filename)
        self.df = pd.read_csv(filename)
        self.validate_columns(self.df)

    def verify_origin(self, filename):
        filetype = 'CSV file'
        if filename[-4:] != ".csv":
            self.build_log(log.error, 'wrong_origin', filename, filetype)
            raise TypeError('Wrong data source. Cannot proceed.')

        self.build_log(log.info, 'origin_type_verified', filename, filetype)
