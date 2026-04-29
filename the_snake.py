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

