from pprint import pformat
from typing import NewType, Self
import gce2.config as c

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
        if self.end_datetime is not None and self.allresults_known():
            return True
        return False

    def allresults_known(self):
        return all([self.game_finished(game) for game in self.games])

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

    def game_exists(self, player1, player2) -> bool:
        tested_game = [
            [
                player1,
                c.SCORE["UNKNOW"]
            ],
            [
                player2,
                c.SCORE["UNKNOW"]
            ]
        ]
        for game in self.games:
            if self.same_game(tested_game, game):
                return True
        return False

    def game_update(self, updated_game: GAME) -> Self | None:
        index = self.index_game(updated_game)
        if index is not None:
            self.games[index] = updated_game
            return self
        return False

    def get_results(self):
        dict_results = {}
        for game in self.games:
            for i in range(0, 2):
                dict_results[game[i][0]] = game[i][1]
        return dict_results

    @staticmethod
    def game_finished(game: GAME):
        if game[0][1] == c.SCORE["LOSE"] and game[1][1] == c.SCORE["WIN"]:
            return True
        elif game[0][1] == c.SCORE["WIN"] and game[1][1] == c.SCORE["LOSE"]:
            return True
        elif game[0][1] == c.SCORE["TIE"] and game[1][1] == c.SCORE["TIE"]:
            return True
        else:
            return False
