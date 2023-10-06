import pygame

from environments.Snake.entities.Block import Block
from environments.Snake.entities.Color import Color
from environments.Snake.entities.Direction import Direction
from environments.Snake.entities.Food import Food
from environments.Snake.utilities import game_start, update_screen, handle_input


class SnakeGame:
    metadata = {"render_modes": ["human", "grid"], "render_fps": 30}

    def __init__(
            self,
            block_size=20,
            fps=30,
            height=40,
            initial_length=4,
            render_mode="human",
            width=40,
    ):
        self.background_color = Color.orange
        self.blocks = None
        self.blocks_x = width
        self.blocks_y = height
        self.body = None
        self.body_color = Color.blue
        self.clock = None
        self.direction = None
        self.food_color = Color.red
        self.food = Food(self.blocks_x, self.blocks_y, self.food_color)
        self.fps = fps
        self.head = None
        self.head_color = Color.purple
        self.initial_length = min(initial_length, width // 2)
        self.render_mode = render_mode
        self.score = 0
        self.screen = None

        Block.size = block_size

    def step(self, direction):

        if direction is None:
            direction = self.direction

        (x, y) = (self.head.x, self.head.y)
        step = Direction.step(direction)
        if (direction == 0 or direction == 1) and (self.direction == 0 or self.direction == 1):
            step = Direction.step(self.direction)
        elif (direction == 2 or direction == 3) and (self.direction == 2 or self.direction == 3):
            step = Direction.step(self.direction)
        else:
            self.direction = direction

        self.head.x += step[0]
        self.head.y += step[1]

        dead = False

        if self.head == self.food.block:
            self.score += 1
            self.grow(x, y)
            self.food.new_food(self.blocks)
        else:
            self.move(x, y)
            for block in self.body:
                if self.head == block:
                    dead = True
            if self.head.x >= self.blocks_x or self.head.x < 0 or self.head.y < 0 or self.head.y >= self.blocks_x:
                dead = True

        return dead

    def reset(self):
        self.score = 0
        self.direction = 3
        self.head = Block(self.blocks_x // 2, self.blocks_y // 2, self.head_color)
        self.body = [self.head.copy(i, 0, self.body_color)
                     for i in range(-self.initial_length, 0)]
        self.blocks = [self.food.block, self.head, *self.body]
        self.food.new_food(self.blocks)

    def render(self, training=False):
        if self.screen is None:
            self.screen, self.clock = game_start(
                self.blocks_x * Block.size, self.blocks_y * Block.size)
        self.clock.tick(self.fps)
        update_screen(self.screen, self)
        if not training:
            handle_input()

    def grow(self, x, y):
        body = Block(x, y, Color.blue)
        self.blocks.append(body)
        self.body.append(body)

    def move(self, x, y):
        tail = self.body.pop(0)
        tail.move_to(x, y)
        self.body.append(tail)

    def close(self):
        pygame.quit()
        pygame.display.quit()
        self.screen = None
        self.clock = None

    def play(self, fps=10, acceleration=True, step=1, frep=10):
        self.fps = fps
        self.reset()

        screen, clock = game_start(
            self.blocks_x * Block.size, self.blocks_y * Block.size)

        while pygame.get_init():
            clock.tick(self.fps)
            d = self.step(handle_input())
            if acceleration == frep:
                self.fps += step
            if d:
                self.reset()
                self.fps = fps

            update_screen(screen, self, True)
