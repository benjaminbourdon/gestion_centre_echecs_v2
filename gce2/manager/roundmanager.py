from gce2 import database
from gce2.model.round import Round


class RoundManager:
    def get_round_by_id(self, doc_id):
        with database.get_connexion_rounds() as json_file:
            round_data = json_file.get(doc_id=doc_id)
            if round_data is not None:
                return Round.deserialize(round_data | {"doc_id": round_data.doc_id})
            else:
                print(f"Aucun tour ne correspond à la recherche doc_id={doc_id}")
