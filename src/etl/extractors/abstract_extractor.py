from abc import ABC, abstractmethod
import logging

log = logging.getLogger('root')


class AbstractExtractor(ABC):
    COLUMNS = {'Row ID', 'Order ID', 'Order Date', 'Ship Date',
               'Ship Mode', 'Customer ID', 'Customer Name', 'Segment',
               'Country', 'City', 'State', 'Postal Code', 'Region',
               'Product ID', 'Category', 'Sub-Category', 'Product Name',
               'Sales'}

    MESSAGES = {
        'extracting': 'Extracting data from {}',
        'excedent_cols': 'Excedent columns in origin file against expected schema. Dropping excedent columns.',
        'missing_cols': 'Missing columns in origin file against expected schema. Cannot proceed extraction.',
        'cols_matched': 'All columns of the origin file match the expected schema.',
        'origin_type_verified': 'The data source {} was verified as a {}',
        'wrong_origin': 'The data source {} is not a {}'
    }

    @abstractmethod
    def import_data(self):
        pass

    def verify_origin(self):
        pass

    def validate_columns(self, df):
        existing_cols = set(df.columns).intersection(self.COLUMNS)
        if len(self.COLUMNS) > len(existing_cols):
            self.build_log(log.error, 'missing_cols')
            raise ValueError

        if len(df.columns) > len(self.COLUMNS):
            self.valid_df = df[existing_cols]
            self.build_log(log.warning, 'excedent_cols')
            return

        self.valid_df = df
        self.build_log(log.info, 'cols_matched')

    def build_log(self, logger, message_key, *args):
        template = self.MESSAGES[message_key]
        message = template.format(*args)
        logger(message, extra={'feature': 'EXTRACT'})
