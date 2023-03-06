from pathlib import Path

from tinydb import TinyDB

from gce2 import config


class Player:
    __slots__ = ("firstname", "lastname", "birthday", "federal_id")

    def __init__(self, **kwargs) -> None:
        for key in self.__slots__:
            setattr(self, key, kwargs[key])

    def __repr__(self) -> str:
        return f"({self.federal_id}) {self.firstname} {self.lastname} {self.birthday}"

    def to_dict(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def serialize(self) -> dict:
        return self.to_dict()

    @classmethod
    def deserialize(cls, data: dict) -> object:
        return cls(**data)

    @classmethod
    def new(cls, **kwargs):
        new_player = cls(**kwargs)

        path = Path(config.PATH_JSONFILE_PLAYER)
        with TinyDB(
            path,
            indent=config.JSON_IDENT,
            encoding=config.ENCODING,
        ) as json_file:
            json_file.insert(new_player.serialize())
            return new_player
