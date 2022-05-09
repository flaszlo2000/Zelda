from typing import cast

from scripts.subclass_register import RegisterMixin
from sqlalchemy.engine import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.schema import Table


def check_tables_on(engine: Engine) -> None:
    inspector = Inspector(engine)
    tables_were_ok = True

    for registered_table_class in RegisterMixin():
        if not hasattr(registered_table_class, "__table__"):
            raise ValueError(f"Type *{registered_table_class}* can't be used here")

        table = cast(Table, registered_table_class.__table__) # type: ignore # sqlalchemy
        if not inspector.has_table(str(table)): # type: ignore # sqlalchemy
            # NOTE: why the hell do i need to convert this into str?
            tables_were_ok = False

            print(f"db does not have: {registered_table_class} table!")
            print("Trying to create it:")

            table.create(bind = engine)
    else:
        if tables_were_ok:
            print("[*] NOTE: Save structure has been checked!")
