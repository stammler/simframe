import types


class SimpleNamespace(types.SimpleNamespace):

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        return (
            (name, member)
            for name, member in self.__dict__.items()
            if not name.startswith("_")
        )
