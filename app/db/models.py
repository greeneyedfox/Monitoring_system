from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class SystemLoad(Base):
    __tablename__ = "system_load"
    id = Column(Integer, primary_key=True, index=True)
    cpu_load = Column(Float, nullable=False)
    ram_load = Column(Float, nullable=False)
    disk_load = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
