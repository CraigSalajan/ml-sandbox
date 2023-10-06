from abc import abstractmethod, ABC


class BaseCommand(ABC):
    ARGS_CONFIG = []

    def __init__(self):
        print("Base Command")

    @abstractmethod
    def execute(self, **kwargs):
        pass

    @classmethod
    def arg_spec(cls, parser):
        for arg_config in cls.ARGS_CONFIG:
            parser.add_argument(*arg_config.get('flags'), **arg_config.get('options'))
