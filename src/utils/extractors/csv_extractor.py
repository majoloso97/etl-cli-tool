import logging
import pandas as pd
from .abstract_extractor import AbstractExtractor

log = logging.getLogger('root')


class CsvExtractor(AbstractExtractor):
    def import_data(self, filename):
        self.build_log(log.info, 'extracting', filename)
        self.df = pd.read_csv(filename)
        self.validate_columns(self.df)
        print(self.valid_df.head())
