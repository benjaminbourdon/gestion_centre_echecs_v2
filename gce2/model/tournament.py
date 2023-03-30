import random
from pprint import pformat
from typing import Self, List

import gce2.config as config
import gce2.exception.exception as e
import gce2.manager.playermanager as pm
import gce2.model.player as p
import gce2.model.round as r


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
        self: Self,
        name: str,
        description: str,
        place: str,
        max_round: int | str,
        start_date: str = None,
        end_date: str = None,
        rounds: List[r.Round] = None,
        doc_id: int = None,
        participants: List[p.Player] = None,
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
        if participants is not None and isinstance(participants, list):
            for participant in participants:
                self.add_participant(participant)

    def __repr__(self):
        return (
            super().__repr__()
            + "\n"
            + pformat(self.to_dict(), indent=4, sort_dicts=False)
        )

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.description}) à {self.place} du {self.start_date} au {self.end_date}."
            f"Tournoi en {self.max_round} tours."
        )

    def can_start(self):
        nb_participants = len(self.participants)
        if nb_participants > 0 and nb_participants % 2 == 0:
            return True
        else:
            return False

    def is_started(self):
        if len(self.rounds) > 0:
            return True
        return False

    @property
    def core_dict(self):
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

    def serialize_rounds(self) -> list:
        return [round.serialize() for round in self.rounds]

    @classmethod
    def deserialize(cls, data: dict) -> object:
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
            raise e.InsertRoundException
        if self.nb_rounds > self.max_round:
            raise e.InsertRoundException
        if self.nb_rounds > 0 and not (self.last_round.iscompleted()):
            raise e.InsertRoundException

        round.tournament = self
        self.rounds.append(round)

    def add_participant(self, participant):
        if isinstance(participant, p.Player):
            self.participants.append(participant)

    def generate_random_games(self):
        nb_participants = len(self.participants)

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
