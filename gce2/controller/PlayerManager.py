from gce2.model.player import Player
from pathlib import Path
from tinydb import TinyDB, Query
from gce2 import config


class PlayerManager:
    def post_player(self, data: dict):
        new_player = Player.new(**data)
        return new_player

    def get_players(self):
        path = Path(config.PATH_JSONFILE_PLAYER)

        with TinyDB(
            path,
            indent=config.JSON_IDENT,
            encoding=config.ENCODING,
        ) as json_file:
            return [Player.deserialize(player_data) for player_data in json_file.all()]

    def get_player(self, federal_id):
        path = Path(config.PATH_JSONFILE_PLAYER)

        with TinyDB(
            path,
            indent=config.JSON_IDENT,
            encoding=config.ENCODING,
        ) as json_file:
            player = Query()
            data = json_file.search(player.federal_id == federal_id)
            return Player.deserialize(data[0])
