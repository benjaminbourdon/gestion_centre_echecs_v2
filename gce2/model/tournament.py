from pprint import pformat


class Tournament:

    CORE_ATTRIBUTES = (
        "name",
        "description",
        "place",
        "start_date",
        "end_date",
        "max_round",
        "doc_id",
    )

    def __init__(
        self, name, description, place, max_round, start_date, end_date, doc_id=None
    ) -> None:

        self.name = name
        self.description = description
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.max_round = max_round
        self.doc_id = doc_id

    def __repr__(self):
        return pformat(self.to_dict(), indent=4, sort_dicts=False)

    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "name": self.name,
            "description": self.description,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "max_round": self.max_round,
        }

    def serialize(self) -> dict:
        return self.to_dict()

    @classmethod
    def deserialize(cls, data: dict) -> object:
        return cls(**data)
