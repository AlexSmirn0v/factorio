import pygame
import os
import sys
from pgm import *
from Units.project_cell_stuff import *
import random
import csv
import sqlite3
pygame.font.init()
font_loc = os.path.join(os.getcwd(), 'Design', 'PressStart2P-Regular.ttf')
header = pygame.font.Font(font_loc, 20)
subheader = pygame.font.Font(font_loc, 15)
main_text = pygame.font.Font(font_loc, 10)
game_name = 'Labtrix'

text_color = pygame.Color('black')
back_color = pygame.Color('#784315')
accent_color = pygame.Color('white')

size = WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption(game_name)


def load_image(name, colorkey=None):
    fullname = os.path.join(os.getcwd(), 'Design', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Window():
    def __init__(self) -> None:
        self.titles = ["Конструктор", "Бур", "Труба"]
        self.images = [load_image(f'{i + 1}.png') for i in range(21)]
        self.tube_converter = {
            [0, 1]: 9,
            [2, 3]: 10,
            [1, 3]: 11,
            [0, 3]: 12,
            [1, 2]: 13,
            [0, 1]: 14
        }
        self.start_screen()

    def terminate(self):
        connect = sqlite3.connect(os.path.join('System', 'bulbs.db'))
        connect.cursor().execute(f'''UPDATE bulbs SET value = {self.bulbs[0]} WHERE name = 'r' ''')
        connect.cursor().execute(f'''UPDATE bulbs SET value = {self.bulbs[1]} WHERE name = 'b' ''')
        connect.close()
        pygame.quit()
        sys.exit()

    def centered(self, obj_width, window_width=WIDTH):
        return (window_width - obj_width) / 2

    def copyright(self, screen):
        copy_text = pygame.font.Font(font_loc, 8)
        text = 'MADE BY George Bekrenev & Alex Smirnov', 'DESIGNED BY Egor Grigorev'
        copy_string1 = copy_text.render(text[0], 0, text_color)
        copy_rect1 = copy_string1.get_rect()
        copy_rect1.x = 20
        copy_rect1.top = HEIGHT - 10 - copy_rect1.height
        screen.blit(copy_string1, copy_rect1)

        copy_string2 = copy_text.render(text[1], 0, text_color)
        copy_rect2 = copy_string2.get_rect()
        copy_rect2.x = WIDTH - copy_rect2.width - 20
        copy_rect2.top = copy_rect1.top
        screen.blit(copy_string2, copy_rect2)

        year = copy_text.render('2023', 1, text_color)
        year_rect = year.get_rect()
        year_rect.x = self.centered(year_rect.width, copy_rect2.x - copy_rect1.x - copy_rect1.width) + copy_rect1.x + copy_rect1.width
        year_rect.top = copy_rect1.top
        screen.blit(year, year_rect)

    def generate_board(self):
        length = 1000
        one_part = length ** 2 // 25
        units = list()
        units.extend([CONVERTER['Песок']] * 15 * one_part)
        units.extend([CONVERTER['Медь-Песок']] * 4 * one_part)
        units.extend([CONVERTER['Железо-Песок']] * 4 * one_part)
        units.extend([CONVERTER['Вода']] * 1 * one_part)
        units.extend([CONVERTER['Уголь-Песок']] * 1 * one_part)
        random.shuffle(units)
        return [[Resource((i, j), units[length * j + i], 5000, self) for i in range(length)] for j in range(length)]


    def bubble_window(self, data:dict):
        while pygame.event.wait().type not in [pygame.QUIT, pygame.MOUSEBUTTONDOWN]:
            b_width, b_height = WIDTH // 3, HEIGHT // 3
            bubble = pygame.Surface((b_width, b_height))
            bubble.fill(back_color)
            pygame.draw.rect(bubble, text_color, (0, 0, b_width, b_height), 1, 3)
            text_coord = 20
            for key in data.keys():
                string_rendered = subheader.render(f'{key}: {data[key]}', 1, text_color)
                rectangle = string_rendered.get_rect()
                text_coord += 10
                rectangle.top = text_coord
                rectangle.x = 20
                text_coord += rectangle.height
                bubble.blit(string_rendered, rectangle)

            screen.blit(bubble, (self.centered(b_width), self.centered(b_height, HEIGHT)))
            pygame.display.flip()
        screen.fill(back_color)
        pygame.display.flip()

    def status_panel(self, screen: pygame.Surface, error=None):
        stat_pan_side = 60
        stat_pan = pygame.Surface((self.square_side, stat_pan_side))
        stat_pan.fill(back_color)
        if not error:
            r_icon = pygame.transform.scale(self.images[20], (stat_pan_side, stat_pan_side))
            b_icon = pygame.transform.scale(self.images[19], (stat_pan_side, stat_pan_side))
            stat_pan.blit(r_icon, (0, 0))
            stat_pan.blit(b_icon, (self.square_side / 2, 0))
            r_text = header.render(str(self.bulbs[0]), 1, text_color)
            rectangle = r_text.get_rect()
            rectangle.top = 20
            rectangle.x = stat_pan_side + 5
            stat_pan.blit(r_text, rectangle)

            b_text = header.render(str(self.bulbs[1]), 1, text_color)
            rectangle = b_text.get_rect()
            rectangle.top = 20
            rectangle.x = self.square_side / 2 + stat_pan_side + 5
            stat_pan.blit(b_text, rectangle)
        else:
            string_rendered = subheader.render(self.titles[0], 1, text_color)
            rectangle = string_rendered.get_rect()
            rectangle.top = 5
            rectangle.x = self.centered(rectangle.width, self.square_side)
            stat_pan.blit(string_rendered, rectangle)

        screen.blit(stat_pan, (WIDTH - self.square_side - 10, 5))

    def left_panel(self, screen: pygame.Surface, pan_status: list=[False * 15]):
        panels = list()
        pan_height, pan_width = (HEIGHT - 50) // len(self.titles), WIDTH - HEIGHT + 80
        for i in range(len(self.titles)):
            a = pygame.Surface((pan_width, pan_height))
            panels.append(a)
            if pan_status[i]:
                a.fill(accent_color)
            else:
                a.fill(back_color)
            
            string_rendered = subheader.render(self.titles[i], 1, text_color)
            rectangle = string_rendered.get_rect()
            rectangle.top = self.centered(rectangle.y, pan_height)
            rectangle.x = 10
            a.blit(string_rendered, rectangle)

            image1 = pygame.transform.scale(self.images[CONVERTER[self.titles[i]] - 1 if i != 2 else 9], (pan_height - 40, pan_height - 40))
            a.blit(image1, (pan_width - pan_height + 40, 20))

            screen.blit(a, (0, i * pan_height + 10))

    def decider(self, pan_chosen, pos):
        x, y = pos
        building = pan_chosen
        if building == 0: #Конструктор
            resources = list()
            for neighbor in [self.board[y - 1][x],
                            self.board[y + 1][x],
                            self.board[y][x + 1],
                            self.board[y][x - 1]]:
                if type(neighbor) == Tube:
                    resources.append(neighbor.resource)
            return Factory(pos, )
        elif building == 1: #Бур
            if self.board[y][x].main_type == 0:
                type = self.board[y][x].type
                return Miner(pos, pos, type, self.board)
        elif building == 2: #Труба
            isDiscovered = False
            for neighbor in [self.board[y - 1][x],
                            self.board[y + 1][x],
                            self.board[y][x + 1],
                            self.board[y][x - 1]]:
                if type(neighbor) == Tube or type(neighbor) == Miner and not isDiscovered:
                    isDiscovered = True
                    #resource = neighbor.resource
                    tiles_pos = neighbor.tiles_pos
                elif type(neighbor) == Tube or type(neighbor) == Miner:
                    return False
            return Tube(pos, tiles_pos, self.board)


    def main_window(self, isNew=True):
        screen.fill(back_color)
        UPDATER =  pygame.USEREVENT + 1
        pygame.time.set_timer(UPDATER, 1000)
        if isNew:
            self.board = self.generate_board()
        else:
            self.board = list()
            with open("board.csv", encoding='utf8') as file:
                reader = csv.reader(file, delimiter=';', quotechar='"')
                for row in reader:
                    temp_keep = list()
                    line = list()
                    for element in row:
                        if len(temp_keep) != 3:
                            temp_keep.append(element)
                        else:
                            line.append(CONVERTER[int(temp_keep[0])](int(temp_keep[1]), int(temp_keep[2])))
                    self.board.append(line)
        
        self.square_side = HEIGHT - 100
        square = pygame.Surface((self.square_side, self.square_side))
        square.fill(accent_color)
        l, d = 490, 490
        r, u = 510, 510
        ticker = 0
        pan_status = [False for _ in range(len(self.titles))]
        pan_chosen = '0'
        while True:
            koef = (r - l) // 20 + 1
            self.bulbs = [0, 0]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEWHEEL:
                    l1 = l + event.y * koef
                    r1 = r - event.y * koef
                    d1 = d + event.y * koef
                    u1 = u - event.y * koef
                    if 0 <= l1 <= r1 - 4 and 0 <= d1 <= u1 - 4 and r1 <= 1000 and u1 <= 1000:
                        l, r, d, u = l1, r1, d1, u1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    if WIDTH - self.square_side - 10 <= x <= WIDTH - 10 and HEIGHT - 40 - self.square_side <= y <= HEIGHT - 40:
                        length = r - l
                        self.base_size = self.square_side // length + 1
                        coord_y = d + (y - 60) // self.base_size
                        coord_x = (x - WIDTH + 10 + self.square_side) // self.base_size + l
                        unit = self.board[coord_y][coord_x]
                        if pan_chosen == '0':
                            self.bubble_window(unit.return_status())
                        elif self.decider(pan_chosen, (coord_x, coord_y)):
                            self.board[coord_y][coord_x] = self.decider(pan_chosen, (coord_x, coord_y))
                            
                    elif 0 <= x <= WIDTH - HEIGHT + 80 and 10 <= y <= HEIGHT - 50:
                        which_pan = (y - 10) // ((HEIGHT - 50) // len(self.titles))
                        pan_status[which_pan] = True
                        if which_pan == pan_chosen:
                            pan_chosen = '0'
                        else:
                            pan_chosen = which_pan
                            print(self.titles[pan_chosen])
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and l - koef >= 0:
                        l -= koef
                        r -= koef
                    elif event.key == pygame.K_RIGHT and r + koef <= 1000:
                        l += koef
                        r += koef
                    elif event.key == pygame.K_DOWN and d - koef >= 0:
                        d += koef
                        u += koef
                    elif event.key == pygame.K_UP and u + koef <= 1000:
                        d -= koef 
                        u -= koef 
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 0 <= x <= WIDTH - HEIGHT + 80 and 10 <= y <= HEIGHT - 50:
                        which_pan = (y - 10) // ((HEIGHT - 50) // len(self.titles))
                        pan_status[which_pan] = True
                        for pan in range(len(self.titles)):
                            if pan != which_pan and  pan != pan_chosen:
                                pan_status[pan] = False
                    else:
                        pan_status = [False for _ in range(len(self.titles))]
                        if type(pan_chosen) == int:
                            pan_status[pan_chosen] = True
                elif event.type == UPDATER:
                    for i in range(1000):
                        for j in range(1000):
                            unit = self.board[i][j]
                            unit.update()
                            if type(unit) == Factory:
                                for i in range(2):
                                    self.bulbs[i] += unit.get_colbs()[i]
                    ticker += 1
            self.left_panel(screen, pan_status)
            self.status_panel(screen)
            self.copyright(screen)
            length = r - l
            self.base_size = self.square_side // length + 1
            square.fill(back_color)
            for line in range(d, u):
                for column in range(l, r):
                    unit = self.board[line][column]
                    if type(unit) == Resource:
                        image = self.images[unit.type - 1]
                    else:
                        if type(unit) == Tube:
                            connected_objects = list()
                            for index, neighbor in enumerate([self.board[column - 1][line],
                                            self.board[column + 1][line],
                                            self.board[column][line + 1],
                                            self.board[column][line - 1]]):
                                if type(neighbor) != Resource:
                                    connected_objects.append(index)
                            if len(connected_objects) == 2:
                                image = self.images[self.tube_converter[connected_objects] - 1]
                        else:
                            image = self.images[unit.type - 1]
                    length = r - l
                    self.base_size = self.square_side // length + 1
                    image1 = pygame.transform.scale(image, (self.base_size, self.base_size))
                    coords = [column - l, length - u + line]
                    square.blit(image1, (coords[0] * self.base_size, coords[1] * self.base_size))
            
            screen.blit(square, (WIDTH - self.square_side - 10, HEIGHT - 40 - self.square_side))
            pygame.display.flip()
            clock.tick(20)

    def start_screen(self, back_name=None):
        intro_text = [f"Добро пожаловать в {game_name}", "",
                    "Начать новую игру",
                    "Продолжить играть", 
                    "", 
                    "",
                    "Для перемещения по игровому полю используйте стрелки",
                    "Изменять масштаб поля можно колёсиком мыши",
                    "",
                    "Для того, чтобы построить сооружение, выберите его в левом меню",
                    "Затем кликните на выбранную клетку поля",
                    "",
                    "Вам доступно несколько типов сооружений:",
                    f"{', '.join(map(lambda x: x.lower(), self.titles))}.",
                    "Буры отвечают за добычу ресурсов, трубы - за их транспортировку,",
                    "а генераторы - за переработку ресурсов",
                    "",
                    "И помните - колбы правят миром!!!"
                    ]
        if back_name:
            fon = pygame.transform.scale(load_image(back_name), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
        else:
            screen.fill(back_color)
        rects = list()
        text_coord = 50
        for line in range(len(intro_text)):
            if line < 4:
                string_rendered = header.render(intro_text[line], 1, text_color)
            else:
                string_rendered = subheader.render(intro_text[line], 1, text_color)
            rectangle = string_rendered.get_rect()
            text_coord += 10
            rectangle.top = text_coord
            rectangle.x = self.centered(rectangle.width)
            rects.append(rectangle)
            text_coord += rectangle.height
            screen.blit(string_rendered, rectangle)
            self.copyright(screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEMOTION:
                    for rect in rects:
                        if 0 <= event.pos[0] - rect.x <= rect.width and \
                                0 <= event.pos[1] - rect.y <= rect.height:
                            pygame.draw.rect(screen, accent_color, rect)
                        else:
                            pygame.draw.rect(screen, back_color, rect)
                elif event.type == pygame.KEYDOWN and event.key == 13:
                    running = False
                    self.main_window(True)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 <= event.pos[0] - rects[3].x <= rect.width and \
                                0 <= event.pos[1] - rects[3].y <= rect.height:
                        running = False
                        self.main_window(False)
                    elif 0 <= event.pos[0] - rects[2].x <= rect.width and \
                                0 <= event.pos[1] - rects[2].y <= rect.height:
                        running = False
                        self.main_window(True)
            text_coord = 50
            for line in range(len(intro_text)):
                if line < 4:
                    string_rendered = header.render(intro_text[line], 1, text_color)
                else:
                    string_rendered = subheader.render(intro_text[line], 1, text_color)
                rectangle = string_rendered.get_rect()
                text_coord += 10
                rectangle.top = text_coord
                rectangle.x = self.centered(rectangle.width)
                text_coord += rectangle.height
                screen.blit(string_rendered, rectangle)
            self.copyright(screen)
            pygame.display.flip()
            clock.tick(20)

Window()