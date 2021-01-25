from src.unit_type_resource import UnitTypeResource


class IrregularTypeResource(UnitTypeResource):
    @staticmethod
    def get_icon_path() -> str:
        return 'data/'
