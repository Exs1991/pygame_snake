import pygame, sys, random, pygame_menu

pygame.init()
bg_imege = pygame.image.load('1639232401_1-papik-pro-p-zmeya-klipart-1.png')
FRAME_COLOR = (0, 255, 204)  # цвет, где 1 - красный, 2- зеленый, 3 - синий (оттенки диапозоном 0-255)
White = (255, 255, 255)
BLUE = (204, 255, 255)
BLOCK_SIZE = 20  # размер квадрата на игровом поле
HEDER_MARGIN = 70  # Отступ от вверха экрана
SNAKE_COLOR = (0, 102, 0)
RED = (224, 0, 0)
HEDER_COLOR = (0, 204, 153)
COUNT_BLOCKS = 20  # Количество квадратиков на поле
MARGIN = 1  # отступ между квадратами
TIME_CLOCK = pygame.time.Clock()  # скорость движения обЪекта он же fps
courier = pygame.font.SysFont('comicsansms', 36)
size = [BLOCK_SIZE * COUNT_BLOCKS + 2 * BLOCK_SIZE + MARGIN * COUNT_BLOCKS,
        BLOCK_SIZE * COUNT_BLOCKS + 2 * BLOCK_SIZE + MARGIN * COUNT_BLOCKS + HEDER_MARGIN]  # размер экрана
screen = pygame.display.set_mode(size)  # передача игрового экрана
pygame.display.set_caption("SNAKE")  # заголовок игры


class snake_block:  # класс змейки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):  # функция для проверки границ игры
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):  # функция сравнения, где перменная self будет apple, other будет head
        return isinstance(other,
                          snake_block) and self.x == other.x and self.y == other.y  # если совпадают координаты то


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [BLOCK_SIZE + column * BLOCK_SIZE + MARGIN * (column + 1),
                                     HEDER_MARGIN + BLOCK_SIZE + row * BLOCK_SIZE + MARGIN * (row + 1),
                                     BLOCK_SIZE,
                                     BLOCK_SIZE])  # ресуем поле, 1- где будем приенять, 2 - цвет , 3- размер квадрата


def start_the_game():
    def get_random_block():  # функкция появления яблоко в рандмоном месте
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = snake_block(x, y)
        while empty_block in SNAKE_BLOCK:  # проверка чтобы яблоки не поподали на змейку
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    SNAKE_BLOCK = [snake_block(8, 9), snake_block(9, 9), snake_block(9, 10)]  # Координаты змейки на поле

    apple = get_random_block()
    d_row = buf_row = 0  # Переменные движения змейки
    d_column = buf_column = 1  # Переменные движения змейки
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():  # цикл по обработке событий
            if event.type == pygame.QUIT:  # если тип события выход, то
                pygame.quit()  # # команда на закрытие игрового окна
                sys.exit()  # чтобы при выходе не было ошибки
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_column != 0:  # ПРоверка  движения змейки
                    buf_row = -1
                    buf_column = 0
                elif event.key == pygame.K_DOWN and d_column != 0:
                    buf_row = 1
                    buf_column = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_column = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_column = 1
        screen.fill(FRAME_COLOR)  # применяем цвет к экрану
        pygame.draw.rect(screen, HEDER_COLOR, [0, 0, size[0], HEDER_MARGIN])

        text_total = courier.render(f'TOTAL: {total}', 0, White)
        text_speed = courier.render(f'Speed: {speed}', 0, White)
        screen.blit(text_total, (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(text_speed, (BLOCK_SIZE + 200, BLOCK_SIZE))
        for row in range(COUNT_BLOCKS):  # заполнение поле квадратами
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = White
                    draw_block(color, row, column)
        head = SNAKE_BLOCK[-1]
        if not head.is_inside():  # проверка если голова сталкиваеться с границами игрового экрана закончить игру
            break
            # pygame.quit()  # команда на закрытие игрового окна
            # sys.exit()  # чтобы при выходе не было ошибки

        draw_block(RED, apple.x, apple.y)  #

        for block in SNAKE_BLOCK:  # появление блоков на поле
            draw_block(SNAKE_COLOR, block.x, block.y)
        pygame.display.flip()  # активируем цвет (команда применяет все что нарисовано на экране)
        if apple == head:  # съедание яблок
            total += 1
            speed = total // 5 + 1
            SNAKE_BLOCK.append(apple)
            apple = get_random_block()

        d_row = buf_row
        d_column = buf_column
        new_head = snake_block(head.x + d_row, head.y + d_column)  # движение головы
        if new_head in SNAKE_BLOCK:
            break
            # pygame.quit()  # команда на закрытие игрового окна
            # sys.exit()  # чтобы при выходе не было ошибки
        SNAKE_BLOCK.append(new_head)  # перемещение головы в хвост при движении
        SNAKE_BLOCK.pop(0)  # удаление последнего символа тоесть хвоста
        TIME_CLOCK.tick(5 + speed)  # активируем команду fps где значение это скорость


menu = pygame_menu.Menu('', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Имя :', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)
while True:

    screen.blit(bg_imege, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
