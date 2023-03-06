class Player:
    __slots__ = ("firstname", "lastname", "birthday", "federal_id")

    def __init__(self, **kwargs) -> None:
        for key in self.__slots__:
            setattr(self, key, kwargs[key])

    def to_dict(self):
        return {key: getattr(self, key) for key in self.__slots__}
