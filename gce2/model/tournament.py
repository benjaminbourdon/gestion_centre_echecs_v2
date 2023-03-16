from pprint import pformat
from gce2.model.round import Round
from gce2.model.player import Player
import gce2.manager.roundmanager as rm
import gce2.manager.playermanager as pm


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
        name,
        description,
        place,
        max_round,
        start_date,
        end_date,
        rounds=None,
        doc_id=None,
        participants=None,
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

    @property
    def core_dict(self):
        return {
            attribute: getattr(self, attribute) for attribute in self.CORE_ATTRIBUTES
        }

    def to_dict(self):
        return (
            {"doc_id": self.doc_id}
            | self.core_dict
            | {"rounds": [round.name for round in self.rounds]}
            | {
                "participants": [
                    participant.doc_id for participant in self.participants
                ]
            }
        )

    def serialize(self) -> dict:
        round_list = [round.doc_id for round in self.rounds if round.doc_id is not None]
        participant_list = [participant.doc_id for participant in self.participants]
        return (
            self.core_dict | {"rounds": round_list} | {"participants": participant_list}
        )

    @classmethod
    def deserialize(cls, data: dict) -> object:
        initializing_data = {
            attribute: data[attribute] for attribute in cls.CORE_ATTRIBUTES
        }
        if "doc_id" in data:
            initializing_data["doc_id"] = int(data["doc_id"])
        tournament = cls(**initializing_data)
        if "rounds" in data:
            round_manager = rm.RoundManager()
            for round_id in data["rounds"]:
                round = round_manager.get_round_by_id(round_id)
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
        if not (isinstance(round, Round)):
            raise BaseException
        if self.nb_rounds > self.max_round:
            raise BaseException
        if self.nb_rounds > 0 and not (self.last_round.iscompleted()):
            raise BaseException
        self.rounds.append(round)

    def add_participant(self, participant):
        if isinstance(participant, Player):
            self.participants.append(participant)
