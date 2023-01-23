import os
import shutil


CONVERTER = {'Уголь': 1,
             'Железо': 2,
             'Медь': 3,
             'Железная-Пластина': 4,
             'Медный-Провод': 5,
             'Конструктор': 6,
             'Бур': 7,
             'Помпа': 8,
             'Труба-Верт': 9,
             'Труба-Горизонт': 10,
             'Труба-Лево-Верх': 11,
             'Труба-Лево-Низ': 12,
             'Труба-Верх-Право': 13,
             'Труба-Низ-Право': 14,
             'Песок': 15,
             'Уголь-Песок': 16,
             'Железо-Песок': 17,
             'Медь-Песок': 18,
             'Вода': 19,
             'Колба-Син': 20,
             'Колба-Красн': 21,
             'Труба-Общ': 22,
             'Генератор': 23}


direct = os.path.join(os.getcwd(), 'Design')
for file in os.listdir(direct):
    if '.' in file and file.split('.')[1] == 'png':
        with open(os.path.join(direct, file), 'rb') as picture:
            try:
                key = '-'.join(map(lambda x: x.capitalize(), file.split('.')[0].split()))
                shutil.copyfile(os.path.join(direct, file), os.path.join(direct, str(CONVERTER[key]) + '.png'))
            except KeyError:
                pass


class Resource():
    def __init__(self, coords:tuple, type: int, amount: int) -> None:
        self.coords = coords

    def type(self):
        return 2

    def resource(self):
        return 1
        
    def update(self, ticker):
        pass

    def status(self):
        return {
            "Вор кораллов": "Карл",
            "X": self.coords[1],
            "Y": self.coords[0]
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
