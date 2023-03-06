from .settings import get_global_settings, set_global_settings
from .db import DbService
from .logging.logger import setup_logger


def initialize_cli():
    settings = get_global_settings()
    init_log_type = settings['LOG_TYPE']
    
    # Create database service to ping db server
    db = DbService()
    if not db.is_active:
        if init_log_type == 'D':
            log = setup_logger('root', 'C')
            settings = set_global_settings(LOG_TYPE='C')
            log.critical("Can't reach database server.\n \
                         Defaulting log-type to Console [C].\n \
                         Use etl config to check database credentials.",
                            extra={'feature': 'CLI CONFIG'})
        else:
            log = setup_logger('root', init_log_type)
            log.critical("Can't reach database server.\n \
                         Use etl config to check database credentials.",
                            extra={'feature': 'CLI CONFIG'})
    else:
        log = setup_logger('root', init_log_type)
    
    return settings, db.is_active
