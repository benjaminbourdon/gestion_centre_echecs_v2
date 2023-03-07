from pprint import pformat
from gce2.model.round import Round


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

    def __repr__(self):
        return (
            super().__repr__()
            + "\n"
            + pformat(self.to_dict(), indent=4, sort_dicts=False)
        )

    @property
    def core_dict(self):
        return {
            attribute: getattr(self, attribute) for attribute in self.CORE_ATTRIBUTES
        }

    def to_dict(self):
        return {"doc_id": self.doc_id} | self.core_dict | {"rounds": [round.name for round in self.rounds]}

    def serialize(self) -> dict:
        round_list = [round.serialize() for round in self.rounds]
        return self.core_dict | {"rounds": round_list}

    def add_rounds_from_json(self, list_rounds):
        if isinstance(list_rounds, list):
            for data_round in list_rounds:
                round = Round.deserialize(data_round)
                self.add_round(round)

    @classmethod
    def deserialize(cls, data: dict) -> object:
        initializing_data = {
            attribute: data[attribute] for attribute in cls.CORE_ATTRIBUTES
        }
        tournament = cls(**initializing_data)
        if "rounds" in data:
            tournament.add_rounds_from_json(data["rounds"])
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
