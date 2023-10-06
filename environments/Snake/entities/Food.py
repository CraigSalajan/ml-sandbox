from random import randint

from environments.Snake.entities.Block import Block


class Food:
    def __init__(self, blocks_x, blocks_y, color) -> None:
        self.blocks_x = blocks_x
        self.blocks_y = blocks_y
        self.block = Block(0, 0, color)

    def new_food(self, blocks):
        (x, y) = (randint(0, self.blocks_x-1), randint(0, self.blocks_y-1))
        done = False

        while not done:
            done = True
            for block in blocks:
                if (x, y) == (block.x, block.y):
                    (x, y) = (randint(0, self.blocks_x-1),
                              randint(0, self.blocks_y-1))
                    done = False
                    break
        self.block.move_to(x, y)
