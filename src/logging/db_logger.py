import logging
from ..core.models import Log
from ..core.db import DbService


class DBHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log = Log(timestamp=record.asctime.replace(',', '.'),
                  feature=record.feature,
                  level=record.levelname,
                  message=record.message)
        db = DbService()
        db.save(log)
