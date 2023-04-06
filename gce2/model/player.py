import re

from dateutil import parser

from gce2.utils import _is_str
import gce2.config as config


class Player:
    CORE_ATTRIBUTES = ("firstname", "lastname", "birthday", "federal_id")
    FEDERALID_PATTERN = "^[A-Z]{2}[0-9]{5}$"

    def __init__(self, **kwargs) -> None:
        for key in self.CORE_ATTRIBUTES:
            setattr(self, key, kwargs[key])

    def __repr__(self) -> str:
        return f"{self.federal_id} : {self.firstname} {self.lastname}, {self.birthday}"

    def __str__(self) -> str:
        return f"{self.federal_id:<9}\t{self.fullname:<25}(né le {self.birthday})"

    def to_dict(self) -> dict[str, str]:
        return {key: getattr(self, key) for key in self.CORE_ATTRIBUTES}

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

    @property
    def federal_id(self):
        return self._federal_id

    @federal_id.setter
    def federal_id(self, value):
        if _is_str(value) and re.match(self.FEDERALID_PATTERN, value):
            self._federal_id = value
        else:
            raise AttributeError(name="federal_id", obj=self)

    @property
    def birthday(self):
        datetime = self._birthday
        return datetime.strftime(config.DATE_FORMAT)

    @birthday.setter
    def birthday(self, value):
        try:
            datetime = parser.parse(value, fuzzy=True, dayfirst=True)
        except parser.ParserError:
            raise AttributeError(name="birthday", obj=self)
        else:
            self._birthday = datetime
