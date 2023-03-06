from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from .settings import get_global_settings
from .models import Base


class DbService:
    def __init__(self) -> None:
        try:
            self.engine = create_engine(self.get_url())
            Base.metadata.create_all(self.engine)
            self.session = sessionmaker(self.engine)
            self.is_active = True
        except Exception:
            self.is_active = False

    def get_url(self):
        settings = get_global_settings()
        url = URL.create(drivername='mysql+pymysql',
                         username=settings['DB_USER'],
                         password=settings['DB_PASS'],
                         host=settings['DB_HOST'],
                         port=settings['DB_PORT'],
                         database=settings['DB_NAME'])
        return url

    def save(self, record):
        with self.session.begin() as session:
            session.add(record)
            session.commit()

    def bulk_save(self, records, cls):
        with self.session.begin() as session:
            session.bulk_insert_mappings(cls, records)
            session.commit()
