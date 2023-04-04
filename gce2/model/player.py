class Player:
    __slots__ = ("firstname", "lastname", "birthday", "federal_id")

    def __init__(self, **kwargs) -> None:
        for key in self.__slots__:
            setattr(self, key, kwargs[key])

    def __repr__(self) -> str:
        return f"{self.federal_id} : {self.firstname} {self.lastname}, {self.birthday}"

    def __str__(self) -> str:
        return f"{self.federal_id:<9}\t{self.fullname:<25}(né le {self.birthday})"

    def to_dict(self) -> dict[str, str]:
        return {key: getattr(self, key) for key in self.__slots__}

    def serialize(self) -> dict:
        return self.to_dict()

    @classmethod
    def deserialize(cls, data: dict) -> object:
        return cls(**data)

    @staticmethod
    def federalid_to_int(federal_id) -> int:
        doc_id = []
        for caracter in federal_id:
            if not caracter.isdigit():
                caracter = str(ord(caracter))
            doc_id.append(caracter)
        return int("".join(doc_id))

    @property
    def doc_id(self):
        return self.federalid_to_int(self.federal_id)

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
