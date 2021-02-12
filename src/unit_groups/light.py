from src.unit_group import UnitGroup


class LightGroup(UnitGroup):
    @staticmethod
    def get_priority() -> int:
        return 1
