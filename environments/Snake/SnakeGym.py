import gymnasium as gym
import numpy as np

from gymnasium import spaces

from environments.Snake.entities.Direction import Direction
from environments.Snake.game_logic import SnakeGame


class SnakeGym(gym.Env):

    def __init__(self):
        self.game = SnakeGame()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            float("-inf"), float("inf"), shape=(self.game.blocks_x * self.game.blocks_y + 1 + 2 + 4,))

    def _build_game_state(self):
        dx = self.game.head.x - self.game.food.block.x
        dy = self.game.head.y - self.game.food.block.y

        # Normalize Manhattan distance
        max_distance = self.game.blocks_x + self.game.blocks_y  # max possible Manhattan distance
        distance_to_food = (abs(dx) + abs(dy)) / max_distance
        d1, d2 = Direction.step(int(self.game.direction))

        board_state = np.zeros((self.game.blocks_x, self.game.blocks_y), dtype=np.int32)

        # Food
        fx, fy = self.game.food.block.x, self.game.food.block.y
        if 0 <= fx < self.game.blocks_x and 0 <= fy < self.game.blocks_y:
            board_state[fx][fy] = 2

        # Snake body
        for block in self.game.body:
            bx, by = block.x, block.y
            if 0 <= bx < self.game.blocks_x and 0 <= by < self.game.blocks_y:
                board_state[bx][by] = 1

        # Snake head
        hx, hy = self.game.head.x, self.game.head.y
        if 0 <= hx < self.game.blocks_x and 0 <= hy < self.game.blocks_y:
            board_state[hx][hy] = 3

        # Flatten the board state
        flattened_board = board_state.flatten()

        # Snake's Direction as one-hot encoded vector
        # Assuming self.direction is between 0 and 3, representing Up, Down, Left, Right
        direction_vector = [0, 0, 0, 0]
        direction_vector[self.game.direction] = 1

        # Combine the flattened board state with the direction vector
        observation = np.concatenate([flattened_board, direction_vector])
        observation = np.concatenate([observation, [distance_to_food, d1, d2]])
        return observation, {}

    def _calculate_reward(self):
        return 1

    def step(self, action):
        done = self.game.step(action)
        game_state, info = self._build_game_state()
        reward = self._calculate_reward()

        self.render()
        return game_state, reward, done, False, info

    def reset(self, seed=None, options=None):
        self.game.reset()

        return self._build_game_state()

    def render(self):
        self.game.render(True)

    def close(self):
        self.game.close()

    def play(self):
        self.game.play()
