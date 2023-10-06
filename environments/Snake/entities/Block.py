class Block:
    size = 20

    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.color = color

    def copy(self, dx, dy, color=None):
        if color is None:
            color = self.color
        return Block(self.x+dx, self.y+dy, color)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    @property
    def rect(self):
        return self.x * Block.size, self.y * Block.size, Block.size, Block.size
