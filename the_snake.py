from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс, от которого наследуются все объекты.
    Содержит общие атрибуты: позиция и цвет.
    """

    def __init__(self, position=None, body_color=None):
        """
        Конструктор базового игрового объекта.
        Аргументы: position (координаты), body_color (цвет).
        """
        if position is None:
            self.position = (320, 240)
        else:
            self.position = position

    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта на экране.
        Аргумент: surface(поверхность, на которой рисуем).
        """        
        pass

class Apple(GameObject):
    """
    Класс Apple. Наследуется от GameObject.
    Появлется в случайном месте поля.
    """    

    super.__init__(position=None, body_color=APPLE_COLOR)

    self.radomize_position()

    def radomize_position(self):
        """
        Устанавливает случайные координаты для яблока.
        """
        max_x = 640 - 20
        max_y = 480 - 20

        x.random.randrage(0, max_x + 1, 20)
        y.random.randrage(0, max_y + 1, 20)

        self.position = (x, y)

    def draw(self, surface):
        """
        Отрисовывает яблоко на игровом поле. 
        """

        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            20,
            20
        )

        pygame.draw.rect(surface, self.body_color, rect)

class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        # Начальная позиция: центр экрана (состоит из одного сегмента)
        start_x = GRID_WIDTH // 2 * GRID_SIZE
        start_y = GRID_HEIGHT // 2 * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None          # Позиция последнего сегмента перед движением (для затирания)
        super().__init__(body_color=SNAKE_COLOR)

    def update_direction(self):
        """Обновляет направление движения, если новое направление не противоположно текущему."""
        if self.next_direction:
            # Запрещаем разворот на 180 градусов
            if (self.next_direction[0] != -self.direction[0] or
                self.next_direction[1] != -self.direction[1]):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self, ate_apple=False):
        """Перемещает змейку. Если ate_apple=True, то сегмент не удаляется."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        self.positions.insert(0, new_head)
        if not ate_apple:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Рисует змейку. Хвост затирается через self.last."""
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        # Затираем последний сегмент, если змейка не удлинилась
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def check_collision(self):
        """Проверяет столкновение головы с границами поля или с телом."""
        head = self.positions[0]
        # Выход за границы
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or
            head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            return True
        # Самопересечение (голова столкнулась с любым другим сегментом)
        if head in self.positions[1:]:
            return True
        return False

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def get_positions(self):
        """Возвращает список всех сегментов для проверки свободных клеток."""
        return self.positions


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
                


def main():
    # Создаём объекты игры
    snake = Snake()
    apple = Apple(snake.get_positions())

     while True:
        clock.tick(SPEED)
        handle_keys(snake)

         # Обновляем направление и двигаем змейку
        snake.update_direction()
        ate = (snake.get_head_position() == apple.position)
        snake.move(ate)

        # Если съели яблоко, создадим новое
        if ate:
            apple.snake_positions = snake.get_positions()
            apple.randomize_position()

        # Проверка столкновения (своё тело или границы)
        if snake.check_collision():
            print("Game Over!")
            pygame.quit()
            break

        # Отрисовка всего
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':

main()

