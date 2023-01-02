CONVERTER = {
    'forest': 1,
    'resource': 2
}


class Resource():
    def __init__(self, type: int, amount: int) -> None:
        pass

    def type(self):
        return 2

    def resource(self):
        return 1
        
    def update(self, ticker):
        pass

    def status(self):
        return {
            'abra': 'cadabra',
            'кто убил Марка': "Карл",
            "Параметр": 20000,
            "Возраст ежей": 3
        }


class Miner():
    def __init__(self, location: tuple) -> None:
        pass

    def update(self, ticker):
        pass


class Factory():
    def __init__(self, *args) -> None:
        pass
    
    def update(self, ticker):
        pass


class Tube():
    def __init__(self, location: tuple) -> None:
        pass
    
    def update(self, ticker):
        pass