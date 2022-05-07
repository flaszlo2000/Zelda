from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Optional, Type, TypeVar

from sqlalchemy.orm import Session, sessionmaker

from db.handlers.base import DbHandler
from db.models.base import DbModel
from db.models.settings import Settings

DB_URI = "sqlite:///dist/saves/save.db" #! FIXME

T = TypeVar("T")
class SaveSystemBase(ABC):
    def __init__(self, db_handler: Optional[DbHandler] = None):
        if db_handler is None:
            self.db_handler = DbHandler(DB_URI)
        else:
            self.db_handler = db_handler

    @abstractmethod
    def saveValue(self, db_model: DbModel) -> bool:...

    def loadValue(self, value_key: str, required_type: Type[T]) -> T:...

    def saveGame(self) -> None:...

    def loadGame(self) -> None:...


@contextmanager
def session_handler(session_maker: sessionmaker) -> Generator[Session, None, None]:
    session: Session = session_maker()
    yield session
    session.commit()
    session.close()

class SaveSystem(SaveSystemBase):
    def saveValue(self, db_model: DbModel) -> bool:
        session_maker = self.db_handler.getSessionmaker()
        with session_handler(session_maker) as session:
            has_the_vallue = session.query(db_model.__class__)
            print(has_the_vallue)

        return False


class SaveSystemWrapper(SaveSystem):
    def updateMusicOnStartup(self, state: bool) -> None:
        self.saveValue(
            Settings(name="musicOnStartUp", value=str(state))
        )

if __name__ == "__main__":
    test_save_sys = SaveSystemWrapper()
    test_save_sys.updateMusicOnStartup(False)
