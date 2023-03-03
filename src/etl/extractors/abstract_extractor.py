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
        'cols_not_matching': 'Not all columns of the origin file match the expected schema.',
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
