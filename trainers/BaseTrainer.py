import pprint
from abc import ABC, abstractmethod

import torch
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv

from di.injector import base_class


@base_class
class BaseTrainer(ABC):

    def get_name(self):
        if self._name:
            return self._name

        return None

    def __init__(self):
        self._name = None
        self.env = None
        self.training_algorithm = None
        self.config = None
        self.game_parameters = None
        self.model_parameters = None

    def train(self, config):
        self.config.update(config)
        pprint.pprint(config)
        if torch.cuda.is_available():
            print(torch.cuda.get_device_name())
        else:
            print("CPU Training")

        # run = self.wandb_init()
        env = self._get_env()

        # if self.config.get("run_id") is not None:
        #     model, _ = self._get_model(self.config.get("run_id"), env, None, None)
        # else:
        model = self._create_model(env)

        callbacks = []
        # checkpoint = CheckpointCallback(
        #     save_freq=50000,
        #     save_path=f"{self.model_save_path}/{self.project_name}/{run.id}",
        #     name_prefix="training_timesteps_",
        #     save_replay_buffer=True,
        #     save_vecnormalize=True
        # )
        # callbacks.append(checkpoint)

        # if self.wandb:
        #     wandb_callback = WandbCallback(
        #         gradient_save_freq=50000,
        #         model_save_path=f"{self.model_save_path}/{self.project_name}/{run.id}",
        #         verbose=2,
        #     )
        #     callbacks.append(wandb_callback)

        model.learn(
            total_timesteps=self.config.get("total_timesteps"),
            callback=callbacks
        )

        # model.save(f"{self.model_save_path}/{self.project_name}/{run.id}/final.pt")

        # if self.wandb:
        #     wandb.finish()

    @abstractmethod
    def play(self, **kwargs):
        pass

    def _filter_config(self, parameters):
        return {k: v for k, v in self.config.items() if k in parameters}

    def _create_env(self):
        if self.env:
            def _init():
                return Monitor(self.env(**self._filter_config(self.game_parameters)))

            return _init

    def _get_env(self):
        envs = [self._create_env() for _ in range(self.config.get("num_envs"))]
        env = SubprocVecEnv(envs)

        return env

    def _create_model(self, env):
        if self.training_algorithm:
            return self.training_algorithm(
                device="cuda",
                env=env,
                **self._filter_config(self.model_parameters)
            )
