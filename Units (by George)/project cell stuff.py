import pygame

if __name__ == '__main__':
    pygame.init()
    size = 800, 800
    screen = pygame.display.set_mode(size)

    board = [[[0, 0], [0, 0]],
             [0, 0], [0, 0],
             [0, 0], [0, 0],
             [0, 0], [0, 0],
             [0, 0], [0, 0]]


    class Board:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            self.left = 5
            self.top = 5
            self.cell_size = 10

        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size

        # def get_cell(self, mouse_pos):
        #    mouse_x, mouse_y = mouse_pos
        #    cell_x = (mouse_x - self.left) // self.cell_size
        #     cell_y = (mouse_y - self.top) // self.cell_size
        #    if cell_x < 0 or cell_y < 0 or cell_x >= self.width or cell_y >= self.height:
        #        print(None)
        #        return None
        #    print((cell_x, cell_y))
        #     return cell_x, cell_y

        # def on_click(self, cell_pos):
        #     x, y = cell_pos
        #       self.board[y][x] = not bool(self.board[y][x])

        # def get_click(self, mouse_pos):
        #    cell = self.get_cell(mouse_pos)
        #    if cell != None:
        #        self.on_click(cell)

        def render(self, screen):
            for x in range(self.width):
                for y in range(self.height):
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        (
                            self.left + x * self.cell_size,
                            self.top + y * self.cell_size,
                            self.cell_size,
                            self.cell_size
                        ),
                        1
                    )

        # def next_move(self):
        #    tmp_board = copy.deepcopy(self.board)
        #  for y in range(self.height):
        #      for x in range(self.width):


    #
    #          for i in range(-1, 2):
    #              for j in range(-1, 2):
    #                  if y + i < 0 or y + i >= self.height or x + j < 0 or x + j >= self.width:
    #                     print("poop")

    class Resource:
        def __init__(self, pos, type, resamount):
            self.type = type
            self.pos = pos
            self.resamount = resamount
            self.status = (type, resamount)

        def return_status(self):
            return self.status

        def empty(self):
            pass
            # изменяет текстурку когда ресурс исчерпан и делает обычной землей?

        def update(self):
            pass



    class Factory:
        def __init__(self, pos, minerpos, type):
            self.miners = minerpos
            self.type = type
            self.pos = pos
            self.miner_stats = board[minerpos[1]][minerpos[0]]
            # тут тоже, мне нужно додумать как толком обращатся к словарям

        def return_status(self):
            return self.miner_stats

        def update(self):
            board[self.miners[1]][self.miners[0]][0] -=1 #тут будет из словаря брать сколько нужно материала


    class Miner:
        def __init__(self, pos, respos, type):
            self.respos = respos
            self.type = type
            self.pos = pos
            self.res_stats = board[respos[1]][respos[0]]

        def return_status(self):
            return self.res_stats

        def update(self):
            board[self.pos[1]][self.pos[0]][1] -= 1
            board[self.respos[1]][self.respos[0]][1] += 1
            # немного подправить


    class Tube:
        def __init__(self, pos):
            self.pos = pos
            #еще доделываю проверку, не успел дописать

            # тут я также когда доделаю обращение к полю обхожу четыре клетки и запоминаю координаты первой найденной трубы

        def orientation(self):
            # исходя из найденных координат я возвращаю две координаты
            pass


    mainboard = Board(1000, 1000)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #    board.get_click(event.pos)
        screen.fill((0, 0, 0))
        mainboard.render(screen)
        pygame.display.flip()

    pygame.quit()
