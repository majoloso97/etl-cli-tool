from sqlalchemy import (Column, Integer,
                        String, DateTime,
                        Float)
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Log(Base):
    __tablename__ = "etl_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime())
    feature = Column(String(15))
    level = Column(String(10))
    message = Column(String(150))


class SalesRecord(Base):
    __tablename__ = "sales_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(20))
    order_date = Column(DateTime())
    order_year = Column(Integer())
    ship_date = Column(DateTime())
    ship_year = Column(Integer())
    ship_mode = Column(TINYINT())
    customer_id = Column(String(20))
    customer_name = Column(String(50))
    segment = Column(TINYINT())
    country = Column(TINYINT())
    city = Column(String(20))
    state = Column(String(20))
    postal_code = Column(Integer())
    region = Column(TINYINT())
    product_id = Column(String(20))
    category = Column(TINYINT())
    sub_category = Column(String(20))
    product_name = Column(String(150))
    sales = Column(Float())
