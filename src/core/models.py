from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Log(Base):
    __tablename__ = "etl_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime())
    feature = Column(String(15))
    level = Column(String(10))
    message = Column(String(150))
