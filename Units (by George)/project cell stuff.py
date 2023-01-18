import pygame

if __name__ == '__main__':
    pygame.init()
    size = 800, 800
    screen = pygame.display.set_mode(size)


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
        def __init__(self, type, resamount):
            self.type = type
            self.resamount = resamount
            self.status = (type, resamount)

        def subtract_resource(self, amount):
            self.resamount -= amount

        def return_status(self):
            return self.status

        def empty(self):
            pass
            #изменяет текстурку когда ресурс исчерпан и делает обычной землей?

        def update(self):
            pass


    class Factory:
        def __init__(self, minerpos, type):
            self.miners = minerpos
            self.type = type
            # тут тоже, мне нужно додумать как толком обращатся к полю  обращение к словарям

        def return_status(self):
            # return status
            pass

        def update(self):
            pass


    class Miner:
        def __init__(self, respos, type):
            self.respos = respos
            self.type = type
            # тут я допишу обращение к полю

        def return_status(self):
            # это мне надо дописать исходя из обращения к полю в иницилизации
            pass

        def update(self):
            pass
            # допишу


    class Tube:
        def __init__(self, pos):
            self.pos = pos
            # тут я также когда доделаю обращение к полю обхожу четыре клетки и запоминаю координаты первой найденной трубы

        def orientation(self):
            # исходя из найденных координат я возвращаю две координаты
            pass


    board = Board(1000, 1000)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #    board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

    pygame.quit()
