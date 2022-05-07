from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


class DbModel:
    id = Column(Integer, primary_key=True, autoincrement=True)

Base = declarative_base()
