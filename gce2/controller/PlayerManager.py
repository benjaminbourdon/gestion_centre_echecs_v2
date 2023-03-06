from gce2.model.player import Player
from tinydb import Query
from gce2 import database


class PlayerManager:
    def post_player(self, data: dict):
        new_player = Player(**data)
        with database.get_connexion_player() as json_file:
            json_file.insert(new_player.serialize())
        return new_player

    def get_players(self):
        with database.get_connexion_player() as json_file:
            return [Player.deserialize(player_data) for player_data in json_file.all()]

    def get_player(self, federal_id):
        with database.get_connexion_player() as json_file:
            player = Query()
            data = json_file.search(player.federal_id == federal_id)
            try:
                return Player.deserialize(data[0])
            except IndexError:
                print(f"Aucun joueur connu n'est lié à l'identifiant fédéral {federal_id}")
