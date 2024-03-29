import random
from pprint import pformat

from dateutil import parser

import gce2.config as config
import gce2.exception.exception as exception
import gce2.manager.playermanager as pm
import gce2.model.player as p
import gce2.model.round as r
from gce2.utils import _is_int


class Tournament:

    CORE_ATTRIBUTES = (
        "name",
        "description",
        "place",
        "start_date",
        "end_date",
        "max_round",
    )

    def __init__(
        self,
        name: str,
        description: str,
        place: str,
        max_round: int | str,
        start_date: str = None,
        end_date: str = None,
        rounds: list[r.Round] = None,
        doc_id: int = None,
        participants: list[p.Player] = None,
    ) -> None:

        self.name = name
        self.description = description
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.max_round = max_round
        self.doc_id = doc_id

        self.rounds = []
        if rounds is not None:
            for round in rounds:
                self.add_round(round)

        self.participants = []
        if participants is not None:
            for participant in participants:
                self.add_participant(participant)

    def __repr__(self):
        return (
            super().__repr__()
            + "\n"
            + pformat(self.to_dict(), indent=4, sort_dicts=False)
        )

    def __str__(self):
        return (
            f"{self.name:<30}\n"
            f"se déroule à {self.place}, du {self.start_date} au {self.end_date}, en {self.max_round} tours.\n"
            f"Description : {self.description}"
        )

    @property
    def start_date(self):
        datetime = self._start_date
        return datetime.strftime(config.DATE_FORMAT)

    @start_date.setter
    def start_date(self, value):
        try:
            datetime = parser.parse(value, fuzzy=True, dayfirst=True)
        except parser.ParserError:
            raise AttributeError(name="start_date", obj=self)
        else:
            self._start_date = datetime

    @property
    def end_date(self):
        datetime = self._end_date
        return datetime.strftime(config.DATE_FORMAT)

    @end_date.setter
    def end_date(self, value):
        try:
            datetime = parser.parse(value, fuzzy=True, dayfirst=True)
        except parser.ParserError:
            raise AttributeError(name="end_date", obj=self)
        else:
            self._end_date = datetime

    @property
    def max_round(self):
        return self._max_round

    @max_round.setter
    def max_round(self, value):
        if _is_int(value) and (int_value := int(value)) > 0:
            self._max_round = int_value
        else:
            raise AttributeError(name="max_round", obj=self)

    def can_start(self) -> bool:
        nb_participants = len(self.participants)
        if nb_participants > 0 and nb_participants % 2 == 0:
            return True
        else:
            return False

    def is_started(self) -> bool:
        if self.nb_rounds > 0:
            return True
        return False

    def is_finished(self) -> bool:
        if self.nb_rounds >= self.max_round and self.last_round.iscompleted():
            return True
        return False

    @property
    def core_dict(self) -> dict[str, str | int]:
        return {
            attribute: getattr(self, attribute) for attribute in self.CORE_ATTRIBUTES
        }

    def to_dict(self):
        return (
            {"doc_id": self.doc_id}
            | self.core_dict
            | {"rounds": [round.serialize() for round in self.rounds]}
            | {
                "participants": [
                    participant.doc_id for participant in self.participants
                ]
            }
        )

    def serialize(self) -> dict:
        round_list = self.serialize_rounds()
        participant_list = [participant.doc_id for participant in self.participants]
        return (
            self.core_dict | {"rounds": round_list} | {"participants": participant_list}
        )

    def serialize_rounds(self) -> list[r.Round]:
        return [round.serialize() for round in self.rounds]

    @classmethod
    def deserialize(cls, data: dict):
        initializing_data = {
            attribute: data[attribute]
            for attribute in cls.CORE_ATTRIBUTES
            if attribute in data
        }
        if "doc_id" in data:
            initializing_data["doc_id"] = int(data["doc_id"])
        tournament = cls(**initializing_data)
        if "rounds" in data:
            for round_data in data["rounds"]:
                round = r.Round.deserialize(round_data)
                tournament.add_round(round)
        if "participants" in data:
            player_manager = pm.PlayerManager()
            for player_id in data["participants"]:
                player = player_manager.get_player(player_id)
                tournament.add_participant(player)
        return tournament

    @property
    def nb_rounds(self):
        return len(self.rounds)

    @property
    def last_round(self):
        idround = self.nb_rounds
        if idround > 0:
            return self.rounds[idround - 1]
        return None

    def add_round(self, round):
        if not (isinstance(round, r.Round)):
            raise exception.InsertRoundException
        if self.nb_rounds > self.max_round:
            raise exception.InsertRoundException
        if self.nb_rounds > 0 and not (self.last_round.iscompleted()):
            raise exception.InsertRoundException

        round.tournament = self
        self.rounds.append(round)

    def add_participant(self, participant):
        if isinstance(participant, p.Player):
            self.participants.append(participant)

    @property
    def participants_names(self) -> dict[str, str]:
        return {
            player.federal_id: f"{player.firstname} {player.lastname}"
            for player in self.participants
        }

    @property
    def nb_participants(self):
        return len(self.participants)

    def generate_random_games(self):
        nb_participants = self.nb_participants

        list_games = []
        order = list(range(nb_participants))
        random.shuffle(order)
        for i in range(nb_participants // 2):
            list_games.append(
                (
                    [
                        self.participants[order[2 * i]].federal_id,
                        config.SCORE["UNKNOW"],
                    ],
                    [
                        self.participants[order[2 * i + 1]].federal_id,
                        config.SCORE["UNKNOW"],
                    ],
                )
            )
        return list_games

    def score_participants(self):
        results = {participant.federal_id: 0 for participant in self.participants}

        for round in self.rounds:
            if round.allresults_known():
                round_results = round.get_results()
                for participant in results:
                    results[participant] += round_results[participant]
        return results

    def generate_ranked_games(self):
        dict_participants = self.score_participants()
        ranked_participants = sorted(
            dict_participants, key=dict_participants.get, reverse=True
        )
        list_games = []
        while len(ranked_participants) > 0:
            player1 = ranked_participants.pop(0)
            player2 = None
            for index, other_player in enumerate(ranked_participants):
                if not self.already_played(player1, other_player):
                    player2 = ranked_participants.pop(index)
                    break
            if player2 is None:
                player2 = ranked_participants.pop(0)

            list_games.append(
                (
                    [
                        player1,
                        config.SCORE["UNKNOW"],
                    ],
                    [
                        player2,
                        config.SCORE["UNKNOW"],
                    ],
                )
            )
        return list_games

    def already_played(self, id_player1, id_player2) -> bool:
        return any([round.game_exists(id_player1, id_player2) for round in self.rounds])
