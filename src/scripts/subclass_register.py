from typing import Any, Iterator, List, Optional, Type


class RegisterMixin(Iterator[Type[Any]]):
    __registry: List[Type[Any]] = list()
    __i = 0

    @staticmethod
    def tryToPutIntoRegistry(cls_to_register: Type[Any]) -> None:
        if cls_to_register not in RegisterMixin.__registry:
            RegisterMixin.__registry.append(cls_to_register)
        else:
            pass # FIXME: should i raise an Exception here?

    @classmethod
    def __init_subclass__(cls) -> None:
        cls.tryToPutIntoRegistry(cls)

    @classmethod
    def register(cls, decorated_class: Type[Any]):
        "Helper method for Sqlalchemy's table classes"
        # NOTE: use this as a class decorator
        # if i use this class for inheritence with sqlalchemy's declarative_base, 
        # then it'll throw metaclass exception.
        # So i take as an example the ABCMeta.register and put the decorated_class' into the registry

        cls.tryToPutIntoRegistry(decorated_class)

        return decorated_class

    def __next__(self) -> Type[Any]:
        result: Optional[Type[Any]] = None

        if RegisterMixin.__i < len(RegisterMixin.__registry):
            result = RegisterMixin.__registry[RegisterMixin.__i]
            RegisterMixin.__i += 1
        else:
            RegisterMixin.__i = 0
            raise StopIteration()

        return result

    def __iter__(self) -> Iterator[Type[Any]]:
        return self

def register_table():
    print("hello")

# NOTE: can we make this more flexible?
# like if a want a AlphabetRegister which only registers it's subclasses and nothing else and
# an another one like OtherRegister which works the same only with it's subclasses
