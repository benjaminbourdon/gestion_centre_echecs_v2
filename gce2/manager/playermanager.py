from tinydb.table import Document

from gce2 import database
from gce2.model.player import Player


class PlayerManager:

    def post_player(self, data: dict):
        try:
            new_player = Player(**data)
        except AttributeError:
            return None
        else:
            with database.get_connexion_player() as json_file:
                doc_toinsert = Document(
                    new_player.serialize(), doc_id=new_player.doc_id
                )
                json_file.insert(doc_toinsert)
            return new_player

    def get_players(self):
        with database.get_connexion_player() as json_file:
            return [Player.deserialize(player_data) for player_data in json_file.all()]

    def get_player(self, federal_id):
        with database.get_connexion_player() as json_file:
            doc_id = Player.federalid_to_int(federal_id)
            data = json_file.get(doc_id=doc_id)
            try:
                player = Player.deserialize(data)
            except AttributeError:
                return None
            except TypeError:
                return None
            else:
                return player
