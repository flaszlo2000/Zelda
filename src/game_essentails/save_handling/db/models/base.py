from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


class DbModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True)


Base = declarative_base()
