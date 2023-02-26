from abc import ABC, abstractmethod
import logging

log = logging.getLogger('root')


class AbstractExtractor(ABC):
    COLUMNS = {'symboling', 'normalized-losses', 'make', 'fuel-type',
               'aspiration', 'num-of-doors', 'body-style', 'drive-wheels',
               'engine-location', 'wheel-base', 'length', 'width',
               'height', 'curb-weight', 'engine-type', 'num-of-cylinders',
               'engine-size', 'fuel-system', 'bore', 'stroke',
               'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg',
               'highway-mpg', 'price'}

    MESSAGES = {
        'extracting': 'Extracting data from {}',
        'cols_not_matching': '''Not all columns of the origin file match the expected schema.''',
        'cols_matched': '''All columns of the origin file match the expected schema.'''
    }

    @abstractmethod
    def import_data(self):
        pass

    def validate_columns(self, df):
        existing_cols = set(df.columns).intersection(self.COLUMNS)
        if self.COLUMNS != existing_cols:
            self.valid_df = df[existing_cols]
            self.build_log(log.warning, 'cols_not_matching')
            return

        self.valid_df = df
        self.build_log(log.info, 'cols_matched')

    def build_log(self, logger, message_key, *args):
        template = self.MESSAGES[message_key]
        message = template.format(*args)
        logger(message, extra={'feature': 'EXTRACT'})
