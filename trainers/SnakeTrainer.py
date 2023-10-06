import pprint

from stable_baselines3 import PPO

from di import register
from environments.Snake.SnakeGym import SnakeGym
from trainers.BaseTrainer import BaseTrainer


@register
class SnakeTrainer(BaseTrainer):

    def __init__(self):
        super().__init__()
        self._name = "snake"
        self.env = SnakeGym

        self.training_algorithm = PPO

        self.config = {
            "death_penalty": -10,
            "dist_reward": 10,
            "ent_coef": 0.02,
            "food_distance_growth_rate": 1.05,
            "food_reward": 25,
            "gae_lambda": 0.95,
            "gamma": 0.99,
            "learning_rate": 1.5e-4,
            "living_bonus": -0.1,
            "max_step": 4096,
            "n_steps": 1024,
            "num_envs": 1,
            "policy": "MlpPolicy",
            "total_timesteps": 100000,
            "vf_coef": 0.5
        }

        self.model_parameters = [
            "ent_coef",
            "gae_lambda",
            "gamma",
            "learning_rate",
            "n_steps",
            "policy",
            "vf_coef",
        ]

        self.game_parameters = [

        ]

    def play(self):
        env = self._create_env()()
        env.unwrapped.play()
