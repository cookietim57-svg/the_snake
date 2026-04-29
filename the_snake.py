import random

import pygame

# Константы :
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)
SPEED = 10

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()



class GameObject:
 """Базовый класс игровых объектов."""
    def __init__(self, position=None, body_color=None):
        """Инициализация позиции и цвета."""
        self.position = position
        self.body_color = body_color

def draw(self, surface):
        """Абстрактный метод отрисовки. Переопределяется в наследниках."""
        pass

class Apple(GameObject):
    """Яблоко, которое увеличивает змейку."""

    def __init__(self, snake_positions):
        """Создаёт яблоко в случайной свободной клетке."""
        super().__init__(body_color=APPLE_COLOR)
        self.snake_positions = snake_positions
        self.randomize_position()
        def randomize_position(self):
        """Устанавливает новую позицию, не занятую змейкой."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in self.snake_positions:
                self.position = (x, y)
                break

    def draw(self, surface):
         """Рисует яблоко (квадрат с рамкой)."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    """Змея которой управляет игрок."""

    def __init__(self):
     """Инициализация: одна клетка в центре, направление вправо."""
        start_x = GRID_WIDTH // 2 * GRID_SIZE
        start_y = GRID_HEIGHT // 2 * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__(body_color=SNAKE_COLOR)

    def update_direction(self):
     """Обновляет направление, запрещая разворот."""
        if self.next_direction:
            is_opposite = (self.next_direction[0] == -self.direction[0]
                           and self.next_direction[1] == -self.direction[1])
            if not is_opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self, ate_apple=False):
         """Перемещает змейку, с учётом телепортации через границы."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        
        # Телепортация через границы
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        if not ate_apple:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Рисует змейку и стирает хвост."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

   def check_self_collision_and_trim(self):
        """
        Проверяет, не укусила ли змейка себя.
        Если да – оставляет только голову (длина 1).
        Возвращает True, если произошло столкновение.
        """
        head = self.positions[0]
        if head in self.positions[1:]:
              # Отбрасываем хвост, оставляем только голову
            self.positions = [head]
            return True
        return False

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def get_positions(self):
         """Возвращает список всех сегментов."""
        return self.positions


def handle_keys(snake):
     """Обрабатывает нажатия клавиш управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
                


def main():
    """Главный цикл игры."""
    snake = Snake()
    apple = Apple(snake.get_positions())

     while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        ate = (snake.get_head_position() == apple.position)
        snake.move(ate)

          # Если съели яблоко – создаём новое
        if ate:
            apple.snake_positions = snake.get_positions()
            apple.randomize_position()

        # Проверяем самопересечение (хвост отбрасывается)
        snake.check_self_collision_and_trim()

        # Отрисовка 
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':

main()

