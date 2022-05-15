from .monster import BaseMonster


class Bamboo(BaseMonster):
    @staticmethod
    def monster_name() -> str:
        return "bamboo"
