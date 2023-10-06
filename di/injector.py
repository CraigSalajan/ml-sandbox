from di.container import DependencyContainer

container = DependencyContainer()


def register(cls):
    """Decorator to register a class with the DI container."""
    container.register(cls)
    return cls


def base_class(cls):
    container.register_base(cls)
    return cls;


def inject(cls):
    """Decorator to auto-inject dependencies into class properties based on type annotations."""
    if '__init__' in cls.__dict__:
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            resolve_dependencies(cls)
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init
    return cls


def resolve_dependencies(target_cls):
    """Internal function to resolve and inject dependencies based on type annotations."""
    for attr_name, attr_type in target_cls.__annotations__.items():
        if attr_name not in target_cls.__dict__:
            instance = container.get(attr_type)
            if instance:
                setattr(target_cls, attr_name, instance)
