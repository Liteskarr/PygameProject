from src.unit_group import UnitGroup


class HeavyGroup(UnitGroup):
    @staticmethod
    def get_priority() -> int:
        return 2
