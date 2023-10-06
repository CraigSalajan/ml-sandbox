from abc import ABC, abstractmethod

from di.injector import base_class


@base_class
class BaseTrainer(ABC):

    def get_name(self):
        if self._name:
            return self._name
        
        return None

    def __init__(self):
        self._name = None
        print("Trainer")

    @abstractmethod
    def train(self, **kwargs):
        pass

