"""
Ресы и всякое такое
"""


class Resourse:
    id: int
    net_worth: int
    name: str
    luxury: bool

    @staticmethod
    def get_price(self, number: int, modifier: int) -> int:
        """
        Возвращает стоимость при продаже
        """

        return (int(self.luxury) * 0.5 + 1) * number * modifier * self.net_worth


class NoneResourse(Resourse):
    """
    Больше заглушек богу заглушек!
    """

    id = -1
    net_worth = 0
    name = "Заглушка"
    luxury = False

    @staticmethod
    def get_price(self, **qwargs) -> int:
        return 0
