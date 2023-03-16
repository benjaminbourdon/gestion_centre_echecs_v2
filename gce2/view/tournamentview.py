from gce2.model.tournament import Tournament


class TournamentView():
    def ask_new_tournament(self):
        data = {}
        print("Merci de renseigner les informations suivantes")
        for field in Tournament.CORE_ATTRIBUTES:
            data[field] = input(f"{field} > ")
        return data

    def list_tournaments(self, list_tournaments):
        if isinstance(list_tournaments, list):
            for tournament in list_tournaments:
                if isinstance(tournament, Tournament):
                    print(tournament)
