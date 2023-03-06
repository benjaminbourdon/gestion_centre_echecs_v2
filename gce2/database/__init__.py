from pathlib import Path
from tinydb import TinyDB
from gce2 import config


def get_connexion_player():
    path = Path(config.PATH_JSONFILE_PLAYER)

    connexion = TinyDB(path, indent=config.JSON_IDENT, encoding=config.ENCODING)

    return connexion
