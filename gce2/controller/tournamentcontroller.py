from gce2.view.tournamentview import TournamentView
from gce2.manager.tournamentmanager import TournamentManager


class TournamentController:
    def __init__(self):
        self.view = TournamentView()
        self.manager = TournamentManager()

    def add_tournament(self):
        data = self.view.ask_new_tournament()
        new_tournament = self.manager.post_tournament(data)
        print(f"Vous avez correctement ajouté le tournoi suivant {new_tournament.name}")

    def print_tournaments(self):
        list_tournaments = self.manager.get_tournaments()
        self.view.list_tournaments(list_tournaments)

    def summerize_tournament(self):
        list_tournament = self.manager.get_tournaments()
        selected_tournament = self.view.select_tournament(list_tournament)
        self.view.print_tournament_details(selected_tournament)

    def print_participants(self):
        list_tournament = self.manager.get_tournaments()
        selected_tournament = self.view.select_tournament(list_tournament)
        self.view.print_tournament_participants(selected_tournament)
