from gce2.model.tournament import Tournament
from gce2.view.menuview import MenuView


class TournamentView:
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

    def select_tournament(self, list_tournament):
        choicies = [(tournament.name, tournament) for tournament in list_tournament]
        menuview = MenuView()
        return menuview.ask_choice(
            choicies,
            msg_intro="Quel tournoi voulez-vous consulter ?",
            msg_action="Indiquer le numéro du tournoi souhaité : ",
        )

    def print_tournament_details(self, tournament):
        if isinstance(tournament, Tournament):
            print(
                f"{tournament.name} : du {tournament.start_date} au {tournament.end_date}"
            )
        else:
            raise BaseException
