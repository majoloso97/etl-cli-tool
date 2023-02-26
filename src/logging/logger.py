import logging


def setup_logger(name):
    template = '[%(asctime)s] %(feature)s | %(levelname)s: %(message)s'
    formatter = logging.Formatter(fmt=template)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
