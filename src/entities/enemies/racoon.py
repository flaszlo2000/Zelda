from .monster import BaseMonster


class Racoon(BaseMonster):
    @staticmethod
    def monster_name() -> str:
        return "racoon"
