from typing import List

from commands.BaseCommand import BaseCommand
from di import register
from trainers.BaseTrainer import BaseTrainer


@register
class TrainCommand(BaseCommand):
    ARGS_CONFIG: List[object] = [
        {
            'flags': ['--game'],
            'options': {
                'type': str,
                'required': True,
                'help': 'ID of the item to delete'
            }
        }
    ]

    trainers: List[BaseTrainer] = []

    def execute(self, game, **kwargs):
        for trainer in self.trainers:
            if trainer.get_name() == game:
                return trainer.train(kwargs)

        return f"No trainer found for {game}."
