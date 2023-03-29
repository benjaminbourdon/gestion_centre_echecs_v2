from pprint import pformat
import gce2.model.tournament as tournament


class Round:

    CORE_ATTRIBUTES = ("name", "start_datetime", "end_datetime", "games")

    def __init__(
        self, name, start_datetime=None, end_datetime=None, games=None, tournament=None
    ) -> None:
        self.name = name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        if games is None:
            self.games = []
        else:
            self.games = games
        self.tournament = tournament

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

    @property
    def tournament(self):
        return self._tournament

    @tournament.setter
    def tournament(self, new_tournament):
        if isinstance(new_tournament, tournament.Tournament):
            self._tournament = new_tournament

    def serialize(self) -> dict:
        return {
            attribute: getattr(self, attribute) for attribute in self.CORE_ATTRIBUTES
        }

    @classmethod
    def deserialize(cls, data):
        return cls(**data)
