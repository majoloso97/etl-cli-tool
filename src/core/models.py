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


class SalesRecord(Base):
    __tablename__ = "sales_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(15))
    order_date = Column(DateTime())
    ship_date = Column(DateTime())
    ship_mode = Column(String(150))
    customer_id = Column(String(10))
    customer_name = Column(String(150))
    segment = Column(String(150))
    country = Column(String(150))
    city = Column(String(150))
    state = Column(String(150))
    postal_code = Column(String(150))
    region = Column(String(150))
    product_id = Column(String(150))
    category = Column(String(150))
    sub_category = Column(String(150))
    product_name = Column(String(150))
    sales = Column(String(150))
