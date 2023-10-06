class Direction:
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    @staticmethod
    def step(dir):
        match dir:
            case 0:
                return Direction.up
            case 1:
                return Direction.down
            case 2:
                return Direction.left
            case 3:
                return Direction.right
