from src.unit_group import UnitGroup


class CavalryGroup(UnitGroup):
    @staticmethod
    def get_priority() -> int:
        return 3