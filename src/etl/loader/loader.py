from src.core.db import DbService
from src.core.models import SalesRecord
import logging

log = logging.getLogger('root')


class Loader:
    COLUMNS = {'order_id', 'order_date', 'ship_date', 'ship_mode',
               'customer_id', 'customer_name', 'segment', 'country',
               'city', 'state', 'postal_code', 'region', 'product_id',
               'category', 'sub_category', 'product_name', 'sales'}

    MESSAGES = {
        'db_connection': 'Starting connection to Database',
        'saving': 'Bulk saving data',
        'complete': 'Save transaction is completed',
        'error': "Data couldn't be loaded. An error occurred during the transaction: {}",
        'not_connected': "Couln't connect to database. Records not being saved."
    }

    def __init__(self, data):
        self.data = data

    def validate_data(self):
        pass

    def load_to_db(self):
        self.build_log(log.info, 'db_connection')
        db = DbService()

        if db.is_active:
            try:
                self.build_log(log.info, 'saving')
                db.bulk_save(records=self.data.to_dict(orient='records'),
                             cls=SalesRecord)
                self.build_log(log.info, 'complete')
            except Exception as e:
                self.build_log(log.error, 'error', e)
        else:
            self.build_log(log.critical, 'not_connected')
            raise ConnectionError

    def load_data(self):
        self.validate_data()
        self.load_to_db()

    def build_log(self, logger, message_key, *args):
        template = self.MESSAGES[message_key]
        message = template.format(*args)
        logger(message, extra={'feature': 'LOAD'})
