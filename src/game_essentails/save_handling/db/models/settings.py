from scripts.subclass_register import RegisterMixin
from sqlalchemy import Column, Text

from .base import Base, DbModel


@RegisterMixin.register
class Settings(DbModel, Base):
    __tablename__ = "settings"

    name = Column(Text, unique=True)
    value = Column(Text)
