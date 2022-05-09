from scripts.subclass_register import RegisterMixin
from sqlalchemy import Column, Text

from .base import Base, DbModel


@RegisterMixin.register
class Setting(DbModel, Base):
    __tablename__ = "settings"

    value = Column(Text)
