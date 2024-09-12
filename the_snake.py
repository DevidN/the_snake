import pygame as pg

from random import choice, randint

import sys


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BLACK = (0, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK

BLUE = (93, 216, 228)
BORDER_COLOR = BLUE

RED = (255, 0, 0)
APPLE_COLOR = RED

GREEN = (0, 255, 0)
SNAKE_COLOR = GREEN

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Игровой объект."""

    def __init__(self,
                 position=CENTER_SCREEN,
                 body_color=None):
        """Объект на игровом поле."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объектов."""
        Apple.randomize_position(self.position)

    def draw_cell(self,
                  body,
                  position,
                  color=None):
        """Отрисовываем ячейки на экране и далее будем пользоваться
        в дочерних классах для отрисовки объектов
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблоко."""

    def __init__(self,
                 positions=[],
                 color=APPLE_COLOR):
        """Присваиваем значения для объекта яблоко."""
        super().__init__(None, color)
        self.randomize_position(positions)

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(screen, self.position, APPLE_COLOR)

    def randomize_position(self, positions):
        """Выбираем случайную позицию для объекта яблоко."""
        self.position = ((randint(0, GRID_WIDTH) * GRID_SIZE),
                         (randint(0, GRID_SIZE) * GRID_SIZE))
        while self.position in positions:
            self.randomize_position(self.position)


class Snake(GameObject):
    """Класс змейка."""

    def __init__(self):
        """Присваиваем значения для объекта змейка."""
        super().__init__(CENTER_SCREEN, SNAKE_COLOR)
        self.reset()

    def update_direction(self,
                         next_direction):
        """Переопределяем направление."""
        self.direction = next_direction

    def move(self):
        """Передвижение змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        self.positions[0] = ((head_x + (dir_x * GRID_SIZE)) % SCREEN_WIDTH,
                             (head_y + (dir_y * GRID_SIZE)) % SCREEN_HEIGHT)

        self.positions.insert(0, self.positions[0])

        self.last = (self.positions.pop()
                     if len(self.positions[1:]) > self.length
                     else None)

    def draw(self):
        """Отрисовка змейки."""
        self.draw_cell(screen, self.get_head_position(), SNAKE_COLOR)

        if self.last:
            self.draw_cell(screen, self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс игры при проигрыше."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(snake: Snake):
    """Обработка нажатий на клавиши в игре."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
                break
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
                break
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
                break
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)
                break


def main():
    """Выполнение цикла игры."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(positions=snake.get_head_position())

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(positions=snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
