
from functools import lru_cache

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


class BaseDbHandler:...

class DbHandler(BaseDbHandler):
    def __init__(self, connection_url: str):
        self.engine = self.getEngine(connection_url)

    @staticmethod
    def getEngine(connection_url: str) -> Engine:
        try:
            engine = create_engine(connection_url)
        except ModuleNotFoundError as exc:
            if "postgresql" in connection_url:
                exc.msg += " Do you have the psql extension?"

            raise 

        return  engine
    
    @lru_cache
    def getSessionmaker(self) -> sessionmaker:
        return sessionmaker(bind=self.engine)
