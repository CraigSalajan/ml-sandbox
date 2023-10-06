from collections import defaultdict
from pydoc import locate


def extract_inner_type(type_annotation) -> str:
    # Convert the type annotation to string and strip outer "typing.List[...]"
    type_str = str(type_annotation)
    if "List[" in type_str:
        return type_str.replace("typing.List[", "").replace("]", "")
    return type_str


class DependencyContainer:
    def __init__(self):
        self._services = {}
        self._implementations = defaultdict(list)
        self._bases = []

    def register(self, key=None, instance=None):
        if key and not instance:
            instance = self.auto_inject(key())
            key = type(instance)

        for interface in self._bases:
            if isinstance(instance, interface):
                self._implementations[interface].append(instance)
                return

        self._services[key] = instance

    def register_base(self, key):
        self._bases.append(key)

    def auto_inject(self, instance):
        annotations = getattr(instance, '__annotations__', {})
        for attr_name, attr_type in annotations.items():
            inner_type = locate(extract_inner_type(attr_type))
            if inner_type in self._implementations:
                setattr(instance, attr_name, self._implementations[inner_type])
        return instance

    def get(self, key):
        if key in self._implementations:
            return self._implementations[key]
        return self._services.get(key)
