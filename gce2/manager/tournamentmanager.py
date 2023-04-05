from gce2 import database
# from gce2.model.round import Round
from gce2.model.tournament import Tournament
# from gce2.exception.exception import InsertRoundException


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
        try:
            new_tournament = Tournament.deserialize(data)
        except AttributeError:
            return None
        else:
            with database.get_connexion_tournament() as json_file:
                doc_id = json_file.insert(new_tournament.serialize())
                new_tournament.doc_id = doc_id
            return new_tournament

    def update_rounds(self, tournament: Tournament):
        with database.get_connexion_tournament() as json_file:
            tournament_id = tournament.doc_id
            json_file.update(
                {"rounds": tournament.serialize_rounds()}, doc_ids=[tournament_id]
            )

    def get_tournament_by_id(self, doc_id: int):
        with database.get_connexion_tournament() as json_file:
            tournament_data = json_file.get(doc_id=doc_id)
            if tournament_data is not None:
                return Tournament.deserialize(
                    tournament_data | {"doc_id": tournament_data.doc_id}
                )
            else:
                return None

    # def add_round_in_tournament(self, id_tournament: int, round_data):
    #     round = Round.deserialize(round_data)
    #     tournament = self.get_tournament_by_id(id_tournament)
    #     if round is None or tournament is None:
    #         return None
    #     else:
    #         try:
    #             tournament.add_round(round)
    #         except InsertRoundException:
    #             raise InsertRoundException
    #         else:
    #             with database.get_connexion_tournament() as json_file:
    #                 json_file.update(
    #                     self._add_unique("rounds", tournament.last_round.serialize()), doc_ids=[id_tournament]
    #                 )
    #             return tournament

    def add_participant_in_tournament(self, id_tournament, id_participant):
        with database.get_connexion_tournament() as json_file:
            json_file.update(
                self._add_unique("participants", id_participant),
                doc_ids=[id_tournament],
            )
        return self.get_tournament_by_id(id_tournament)

    @staticmethod
    def _add_unique(field: str, element):
        """Method for TinyDB operation system wich add a element in a list only if it isn't already present

        Args:
            field (str): field modidified
            element (Any): element to insert
        """

        def transform(doc):
            if element not in doc[field]:
                doc[field].append(element)

        return transform
