from pathlib import Path
from tinydb import TinyDB
from gce2 import config


def _get_connexion(path_jsonfile):
    path = Path(path_jsonfile)
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    connexion = TinyDB(path, indent=config.JSON_IDENT, encoding=config.ENCODING)
    return connexion


def get_connexion_player():
    return _get_connexion(config.PATH_JSONFILE_PLAYER)


def get_connexion_tournament():
    return _get_connexion(config.PATH_JSONFILE_TOURNAMENT)


def get_connexion_rounds():
    return _get_connexion(config.PATH_JSONFILE_ROUNDS)
