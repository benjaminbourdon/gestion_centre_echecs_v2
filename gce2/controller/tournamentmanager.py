from tinydb import operations

from gce2 import database
from gce2.model.round import Round
from gce2.model.tournament import Tournament
from gce2 import config


class TournamentManager:
    def get_tournaments(self):
        with database.get_connexion_tournament() as json_file:
            return [
                Tournament.deserialize(
                    tournament_data | {"doc_id": tournament_data.doc_id}
                )
                for tournament_data in json_file.all()
            ]

    def post_tournament(self, core_data):
        new_tournament = Tournament.deserialize(core_data)
        with database.get_connexion_tournament() as json_file:
            doc_id = json_file.insert(new_tournament.serialize())
            new_tournament.doc_id = doc_id
        return new_tournament

    def get_tournament_by_id(self, doc_id):
        with database.get_connexion_tournament() as json_file:
            tournament_data = json_file.get(doc_id=doc_id)
            if tournament_data is not None:
                return Tournament.deserialize(
                    tournament_data | {"doc_id": tournament_data.doc_id}
                )
            else:
                print(f"Aucun tournoi ne correspond à la recherche doc_id={doc_id}.")

    def add_round_in_tournament(self, id_tournament, round_data):
        round = Round.deserialize(round_data)
        tournament = self.get_tournament_by_id(id_tournament)
        tournament.add_round(round)
        with database.get_connexion_tournament() as json_file:
            table_rounds = json_file.table(config.TABLE_ROUNDS)
            id_round = table_rounds.insert(round.serialize())
            json_file.update(
                operations.add("rounds", [id_round]), doc_ids=[id_tournament]
            )
        tournament.last_round.doc_id = id_round
        return tournament

    def add_participant_in_tournament(self, id_tournament, id_participant):
        with database.get_connexion_tournament() as json_file:
            json_file.update(
                operations.add("participants", [id_participant]),
                doc_ids=[id_tournament],
            )
        return self.get_tournament_by_id(id_tournament)
