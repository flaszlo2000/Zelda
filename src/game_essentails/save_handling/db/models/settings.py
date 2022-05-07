from scripts.subclass_register import RegisterMixin
from sqlalchemy import Column, Integer, Text

from .base import Base, DbModel


@RegisterMixin.register
class Settings(DbModel, Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True)
    value = Column(Text)
