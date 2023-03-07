from pathlib import Path
from tinydb import TinyDB
from gce2 import config


def get_connexion_player():
    path = Path(config.PATH_JSONFILE_PLAYER)
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    connexion = TinyDB(path, indent=config.JSON_IDENT, encoding=config.ENCODING)

    return connexion


def get_connexion_tournament():
    path = Path(config.PATH_JSONFILE_TOURNAMENT)
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    connexion = TinyDB(path, indent=config.JSON_IDENT, encoding=config.ENCODING)

    return connexion
