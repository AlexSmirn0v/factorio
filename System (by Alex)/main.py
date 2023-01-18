import pygame
import os
import sys
from main_wind import Resource, CONVERTER
import random
import csv

pygame.font.init()
font_loc = os.path.join(os.getcwd(), 'Design (by Egor)', 'PressStart2P-Regular.ttf')
header = pygame.font.Font(font_loc, 20)
subheader = pygame.font.Font(font_loc, 15)
main_text = pygame.font.Font(font_loc, 10)

text_color = pygame.Color('black')
back_color = pygame.Color('#784315')
accent_color = pygame.Color('white')

size = WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('''Laboratorio''')


def load_image(name, colorkey=None):
    fullname = os.path.join(os.getcwd(), 'Design (by Egor)', name)
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


image = load_image('Big_logo.png')


def terminate():
    pygame.quit()
    sys.exit()


def centered(obj_width, window_width=WIDTH):
    return (window_width - obj_width) / 2


def copyright(screen):
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
    year_rect.x = centered(year_rect.width, copy_rect2.x - copy_rect1.x - copy_rect1.width) + copy_rect1.x + copy_rect1.width
    year_rect.top = copy_rect1.top
    screen.blit(year, year_rect)


def generate_board():
    board = [[Resource(CONVERTER['forest'], 5000) for _ in range(1000)] for _ in range(1000)]
    return board


def bubble_window(data:dict):
    while pygame.event.wait().type not in [pygame.QUIT, pygame.MOUSEBUTTONDOWN]:
        b_width, b_height = WIDTH // 3, HEIGHT // 3
        bubble = pygame.Surface((b_width, b_height))
        bubble.fill(back_color)
        pygame.draw.rect(bubble, text_color, (0, 0, WIDTH // 3, HEIGHT // 3), 1, 3)
        text_coord = 20
        for key in data.keys():
            string_rendered = subheader.render(f'{key}: {data[key]}', 1, text_color)
            rectangle = string_rendered.get_rect()
            text_coord += 10
            rectangle.top = text_coord
            rectangle.x = 20
            text_coord += rectangle.height
            bubble.blit(string_rendered, rectangle)

        screen.blit(bubble, (centered(b_width), centered(b_height, HEIGHT)))
        pygame.display.flip()
    screen.fill(back_color)
    pygame.display.flip()
    

def left_panel(screen: pygame.Surface, pan_status: list=[False, False, False]):
    titles = ["Фабрика", "Шахта", "Труба"]
    panels = list()
    pan_height, pan_width = (HEIGHT - 50) // 3, WIDTH - HEIGHT + 80
    for i in range(3):
        a = pygame.Surface((pan_width, pan_height))
        panels.append(a)
        if pan_status[i]:
            a.fill(accent_color)
        else:
            a.fill(back_color)
        
        string_rendered = subheader.render(titles[i], 1, text_color)
        rectangle = string_rendered.get_rect()
        rectangle.top = centered(rectangle.y, pan_height)
        rectangle.x = 10
        a.blit(string_rendered, rectangle)

        image1 = pygame.transform.scale(image, (pan_height, pan_height))
        a.blit(image1, (pan_width - pan_height, 0))

        screen.blit(a, (0, i * pan_height + 10))


def main_window(isNew=True):
    screen.fill(back_color)
    UPDATER =  pygame.USEREVENT + 1
    pygame.time.set_timer(UPDATER, 1000)
    if isNew:
        board = generate_board()
    else:
        board = list()
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
                board.append(line)
    
    square_side = HEIGHT - 100
    square = pygame.Surface((square_side, square_side))
    square.fill(accent_color)
    l, d = 490, 490
    r, u = 510, 510
    ticker = 0
    pan_status = [False, False, False]
    pan_chosen = '0'
    while True:
        koef = (r - l) // 20 + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEWHEEL:
                l1 = l + event.y * koef
                r1 = r - event.y * koef
                d1 = d + event.y * koef
                u1 = u - event.y * koef
                if 0 <= l1 <= r1 - 4 and 0 <= d1 <= u1 - 4 and r1 <= 1000 and u1 <= 1000:
                    l, r, d, u = l1, r1, d1, u1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                x, y = event.pos
                if WIDTH - square_side - 10 <= x <= WIDTH - 10 and HEIGHT - 40 - square_side <= y <= HEIGHT - 40:
                    bubble_window(board[y // square_side][x // square_side].status())
                elif 0 <= x <= WIDTH - HEIGHT + 80 and 10 <= y <= HEIGHT - 50:
                    which_pan = (y - 10) // ((HEIGHT - 50) // 3)
                    pan_status[which_pan] = True
                    if which_pan == pan_chosen:
                        pan_chosen = '0'
                    else:
                        pan_chosen = which_pan
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and l - koef >= 0:
                    l -= koef
                    r -= koef
                elif event.key == pygame.K_RIGHT and r + koef <= 1000:
                    l += koef
                    r += koef
                elif event.key == pygame.K_DOWN and d - koef >= 0:
                    d -= koef
                    u -= koef
                elif event.key == pygame.K_UP and u + koef <= 1000:
                    d += koef 
                    u += koef 
                print(l, r, d, u)
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 0 <= x <= WIDTH - HEIGHT + 80 and 10 <= y <= HEIGHT - 50:
                    which_pan = (y - 10) // ((HEIGHT - 50) // 3)
                    pan_status[which_pan] = True
                    for pan in range(len(pan_status)):
                        if pan != which_pan and  pan != pan_chosen:
                            pan_status[pan] = False
                else:
                    pan_status = [False, False, False]
                    if type(pan_chosen) == int:
                        pan_status[pan_chosen] = True
            elif event.type == UPDATER:
                for i in range(1000):
                    for j in range(1000):
                        board[i][j].update(ticker)
                print(ticker)
                ticker += 1
        left_panel(screen, pan_status)
        copyright(screen)
        length = r - l
        base_size = square_side // length + 1
        for line in range(d, u):
            for column in range(l, r):
                unit = board[line][column]
                '''if unit.type() == CONVERTER['resource']:
                    image = load_image(f'.\Design (by Egor)\{unit.resource()}.png')
                else:
                    image = load_image(f'.\Design (by Egor)\{unit.type()}.png')'''
                color = (255 // (column - l + 1), 255 // (u - line), 100)
                imager = pygame.Surface((100, 100))
                imager.fill(pygame.Color(color))
                image1 = pygame.transform.scale(image, (base_size, base_size))
                square.blit(image1, ((column - l) * base_size, (u - line - 1) * base_size))
        
        screen.blit(square, (WIDTH - square_side - 10, HEIGHT - 40 - square_side))
        pygame.display.flip()
        clock.tick(20)


def start_screen(back_name=None):
    intro_text = ["Добро пожаловать в Laboratorio", "",
                  "Начать новую игру",
                  "Продолжить играть"]
    if back_name:
        fon = pygame.transform.scale(load_image(back_name), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
    else:
        screen.fill(back_color)
    rects = list()
    text_coord = 50
    for line in intro_text:
        string_rendered = header.render(line, 1, text_color)
        rectangle = string_rendered.get_rect()
        text_coord += 10
        rectangle.top = text_coord
        rectangle.x = centered(rectangle.width)
        rects.append(rectangle)
        text_coord += rectangle.height
        screen.blit(string_rendered, rectangle)
        copyright(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                for rect in rects:
                    if 0 <= event.pos[0] - rect.x <= rect.width and \
                            0 <= event.pos[1] - rect.y <= rect.height:
                        pygame.draw.rect(screen, accent_color, rect)
                    else:
                        pygame.draw.rect(screen, back_color, rect)
            elif event.type == pygame.KEYDOWN and event.key == 13:
                running = False
                main_window(True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= event.pos[0] - rects[-1].x <= rect.width and \
                            0 <= event.pos[1] - rects[-1].y <= rect.height:
                    running = False
                    main_window(False)
                elif 0 <= event.pos[0] - rects[-2].x <= rect.width and \
                            0 <= event.pos[1] - rects[-2].y <= rect.height:
                    running = False
                    main_window(True)
        text_coord = 50
        for line in intro_text:
            string_rendered = header.render(line, 1, text_color)
            rectangle = string_rendered.get_rect()
            text_coord += 10
            rectangle.top = text_coord
            rectangle.x = centered(rectangle.width)
            text_coord += rectangle.height
            screen.blit(string_rendered, rectangle)
        copyright(screen)
        pygame.display.flip()
        clock.tick(20)


start_screen()