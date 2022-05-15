from .monster import BaseMonster


class Squid(BaseMonster):
    @staticmethod
    def monster_name() -> str:
        return "squid"
