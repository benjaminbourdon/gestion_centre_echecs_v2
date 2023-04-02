from pprint import pformat
from typing import NewType, Self

FEDERAL_ID = NewType("FEDERAL_ID", str)
SCORE = NewType("SCORE", float)
GAME = tuple[tuple[FEDERAL_ID, SCORE], tuple[FEDERAL_ID, SCORE]]


class Round:

    CORE_ATTRIBUTES = ("name", "start_datetime", "end_datetime", "games")

    def __init__(
        self,
        name: str,
        start_datetime: str = None,
        end_datetime: str = None,
        games: list[GAME] = None,
        tournament=None,
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
        from gce2.model.tournament import Tournament

        if isinstance(new_tournament, Tournament):
            self._tournament = new_tournament

    def serialize(self) -> dict:
        return {
            attribute: getattr(self, attribute) for attribute in self.CORE_ATTRIBUTES
        }

    @classmethod
    def deserialize(cls, data):
        return cls(**data)

    def index_game(self, game: GAME) -> int | None:
        for index, existing_game in enumerate(self.games):
            if self.same_game(existing_game, game):
                return index
        return None

    @staticmethod
    def same_game(game1: GAME, game2: GAME) -> bool:
        if game1[0][0] == game1[1][0] or game2[0][0] == game2[1][0]:
            return False
        players_game1 = {game1[0][0], game1[1][0]}
        if game2[0][0] in players_game1 and game2[1][0] in players_game1:
            return True
        return False

    def game_update(self, updated_game: GAME) -> Self | None:
        index = self.index_game(updated_game)
        if index is not None:
            self.games[index] = updated_game
            return self
        return False
