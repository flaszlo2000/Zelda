from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Dict, Generator, Optional, Type, TypeVar

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Query, Session, sessionmaker

from db.check_tables import check_tables_on
from db.handlers.base import DbHandler
from db.models.base import DbModel
from db.models.settings import Settings

DB_URI = "sqlite:///dist/saves/save.db" #! FIXME

T = TypeVar("T")
T_A = TypeVar("T_A", bound=DbModel)
class SaveSystemBase(ABC):
    def __init__(self, db_handler: Optional[DbHandler] = None):
        if db_handler is None:
            self.db_handler = DbHandler(DB_URI)
        else:
            self.db_handler = db_handler

        check_tables_on(self.db_handler.getEngine())

    @abstractmethod
    def saveValue(self, db_model: T_A) -> T_A:...

    def loadValue(self, value_key: str, required_type: Type[T]) -> T:...

    def saveGame(self) -> None:...

    def loadGame(self) -> None:...


@contextmanager
def session_handler(session_maker: sessionmaker, engine: Engine) -> Generator[Session, None, None]:
    session: Session = session_maker()
    yield session
    session.commit()
    session.close()

class SaveSystem(SaveSystemBase):
    @staticmethod
    def filter_dict(raw_dict: Dict[str, T]) -> Dict[str, T]:
        return { key:value for key, value in raw_dict.items() if not key.startswith("_") }  

    def saveValue(self, db_model: T_A) -> T_A:
        session_maker = self.db_handler.getSessionmaker()
        with session_handler(session_maker, self.db_handler.getEngine()) as session:
            value_query: Query[T_A] = session.query(db_model.__class__)
            query_result: Optional[T_A] = value_query.first()

            if query_result is None:
                session.add(db_model) # type: ignore # sqlalchemy
                query_result = db_model
            else:
                value_query.update( # type: ignore # sqlalchemy
                    SaveSystem.filter_dict(db_model.__dict__) # sqlalchemy issue with _sa_instance_state
                )
                #! does it update the result?

        return db_model # because of the method is generic, we had to return something in the same type

class SaveSystemAdapter(SaveSystem):
    def updateMusicOnStartUp(self, state: bool) -> None:
        self.saveValue(
            Settings(name="musicOnStartUp", value=str(state))
        )

if __name__ == "__main__":
    test_save_sys = SaveSystemAdapter()
    test_save_sys.updateMusicOnStartUp(True)
