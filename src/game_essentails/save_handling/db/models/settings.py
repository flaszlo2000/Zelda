from sqlalchemy import Column, Integer, Text

from .base import Base, DbModel


class Settings(DbModel, Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True)
    value = Column(Text)

