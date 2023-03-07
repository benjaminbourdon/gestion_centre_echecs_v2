from pprint import pformat


class Round:
    def __init__(self, name, start_datetime=None, end_datetime=None) -> None:
        self.name = name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def __repr__(self) -> str:
        return (
            super().__repr__()
            + "\n"
            + pformat(self.__dict__, indent=4, sort_dicts=False)
        )

    def iscompleted(self):
        if self.end_datetime is not None:
            return True
        return False

    def serialize(self) -> dict:
        return self.__dict__

    @classmethod
    def deserialize(cls, data):
        return cls(**data)
