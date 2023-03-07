from gce2.model.tournament import Tournament
from gce2 import database


class TournamentManager:
    def get_tournaments(self):
        with database.get_connexion_tournament() as json_file:
            return [
                Tournament.deserialize(
                    tournament_data | {"doc_id": tournament_data.doc_id}
                )
                for tournament_data in json_file.all()
            ]

    def post_tournament(self, data):
        new_tournament = Tournament(**data)
        with database.get_connexion_tournament() as json_file:
            doc_id = json_file.insert(new_tournament.serialize())
            new_tournament.doc_id = doc_id
        return new_tournament
