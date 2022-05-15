from .monster import BaseMonster


class Spirit(BaseMonster):
    @staticmethod
    def monster_name() -> str:
        return "spirit"
