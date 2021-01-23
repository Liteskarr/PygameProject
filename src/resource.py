# TODO: docs

class Resource:
    @staticmethod
    def get_cost() -> float:
        raise NotImplementedError()


class NoneResource(Resource):
    @staticmethod
    def get_cost() -> float:
        return 0
