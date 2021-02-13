from src.unit_group import UnitGroup


class InfantryGroup(UnitGroup):
    @staticmethod
    def get_priority() -> int:
        return 4
