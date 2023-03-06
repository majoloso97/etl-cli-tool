import logging
from .db_logger import DbHandler


def setup_logger(name, type):
    template = '[%(asctime)s] %(feature)s | %(levelname)s: %(message)s'
    formatter = logging.Formatter(fmt=template)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    terminal_handler = logging.StreamHandler()
    terminal_handler.setFormatter(formatter)
    logger.addHandler(terminal_handler)

    if type == 'L':
        file_handler = logging.FileHandler(filename='etl_logs.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if type == 'D':
        db_handler = DbHandler()
        logger.addHandler(db_handler)

    return logger
