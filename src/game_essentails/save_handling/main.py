from abc import ABC, abstractmethod
from contextlib import contextmanager
from copy import copy
from typing import Dict, Generator, Optional, TypeVar

from game_essentails.save_handling.db.check_tables import check_tables_on
from game_essentails.save_handling.db.handlers.base import DbHandler
from game_essentails.save_handling.db.models.base import DbModel
from game_essentails.save_handling.db.models.settings import Setting
from game_essentails.save_handling.db_request_handler import DbRequestHandler
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Query, Session, sessionmaker

from .constants import MUSIC_ON_STARTUP, MUSIC_VOLUME

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

    @abstractmethod
    def getValue(self, db_model: T_A) -> Optional[T_A]:...

    def saveGame(self) -> None:...

    def loadGame(self) -> None:...

    def getSessionmaker(self) -> sessionmaker:
        return self.db_handler.getSessionmaker()

@contextmanager
def session_handler(session_maker: sessionmaker, engine: Engine) -> Generator[Session, None, None]:
    new_session: Session = session_maker(autocommit = False, autoflush = False, bind = engine)
    yield new_session
    new_session.expunge_all() # make query results useable outside the contextmanager
    new_session.close()

class SaveSystem(SaveSystemBase):
    @staticmethod
    def filter_dict(raw_dict: Dict[str, T]) -> Dict[str, T]:
        return { key:value for key, value in raw_dict.items() if not key.startswith("_") }  

    def saveValue(self, db_model: T_A) -> T_A:
        with session_handler(self.getSessionmaker(), self.db_handler.getEngine()) as session:
            value_query: Query[T_A] = session.query(db_model.__class__).filter( # type: ignore # sqlalchemy
                db_model.__class__.name == db_model.name
            )
            query_result: Optional[T_A] = value_query.first()

            if query_result is None:
                session.add(db_model) # type: ignore # sqlalchemy
            else:
                value_query.update( # type: ignore # sqlalchemy
                    SaveSystem.filter_dict(db_model.__dict__) # sqlalchemy issue with _sa_instance_state
                )

            session.commit()

        return db_model # because of the method is generic, we had to return something in the same type

    def getValue(self, db_model: T_A) -> Optional[T_A]:
        result: Optional[T_A] = None
        with session_handler(self.getSessionmaker(), self.db_handler.getEngine()) as session:
            result = session.query(db_model.__class__).filter( # type: ignore # sqlalchemy
                db_model.__class__.name == db_model.name
            ).first()
    
        return result

class SaveSystemAdapter(SaveSystem):
    def __init__(self, db_handler: Optional[DbHandler] = None):
        super().__init__(db_handler)
        self.request_handler = DbRequestHandler(self)

    def updateMusicOnStartUp(self, state: bool) -> None:
        self.saveValue(
            Setting(name = MUSIC_ON_STARTUP, value=str(state))
        )

    def getMusicOnStartUpState(self) -> bool:
        result: bool = False
        db_result = self.getValue(
            Setting(name = MUSIC_ON_STARTUP, value = str(True)) #! FIXME: remove fix value
        )

        if db_result is not None:
            result = getattr(db_result, "value")

        return result
    
    def updateMusicVolume(self, new_volume: int) -> None:
        self.saveValue(
            Setting(name = MUSIC_VOLUME, value = str(new_volume))
        )

if __name__ == "__main__":
    test_save_sys = SaveSystemAdapter()
    test_save_sys.updateMusicOnStartUp(True)
    test_save_sys.updateMusicVolume(75)
    print(test_save_sys.getMusicOnStartUpState())
