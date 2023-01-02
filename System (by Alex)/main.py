import pygame
import os
import sys

FPS = 50
pygame.font.init()
font_loc = os.path.join('.', 'Design (by Egor)', 'PressStart2P-Regular.ttf')
header = pygame.font.Font(font_loc, 20)
subheader = pygame.font.Font(font_loc, 15)
main_text = pygame.font.Font(font_loc, 10)
text_color = pygame.Color('black')
back_color = pygame.Color('#784315')

size = WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('''Labtorio''')


def load_image(name, colorkey=None):
    fullname = os.path.join('.', 'Design (by Egor)', name)
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


def start_screen(back_name=None):
    intro_text = ["Добро пожаловать в Labtorio", "",
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
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = centered(intro_rect.width)
        rects.append(intro_rect)
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        copyright(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                for rect in rects:
                    if 0 <= event.pos[0] - rect.x <= rect.width and \
                            0 <= event.pos[1] - rect.y <= rect.height:
                        pygame.draw.rect(screen, pygame.Color('white'), rect)
                    else:
                        pygame.draw.rect(screen, back_color, rect)
            elif event.type == pygame.KEYDOWN and event.key == 13:
                print('new game')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= event.pos[0] - rects[-1].x <= rect.width and \
                            0 <= event.pos[1] - rects[-1].y <= rect.height:
                    print('old game')
                elif 0 <= event.pos[0] - rects[-2].x <= rect.width and \
                            0 <= event.pos[1] - rects[-2].y <= rect.height:
                    print('new game')
        text_coord = 50
        for line in intro_text:
            string_rendered = header.render(line, 1, text_color)
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = centered(intro_rect.width)
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        copyright(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()