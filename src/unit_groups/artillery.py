from src.unit_group import UnitGroup


class ArtilleryGroup(UnitGroup):
    @staticmethod
    def get_priority() -> int:
        return 2
