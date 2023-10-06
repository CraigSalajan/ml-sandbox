from di import register
from trainers.BaseTrainer import BaseTrainer


@register
class SnakeTrainer(BaseTrainer):

    def __init__(self):
        super().__init__()
        self._name = "snake"
        print("Snake Trainer")

    def train(self):
        print("Training")