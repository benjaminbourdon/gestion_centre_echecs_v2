from gce2.controller.playercontroller import PlayerController
from gce2.controller.tournamentcontroller import TournamentController
from gce2.view.menuview import MenuView


class MenuController:
    def __init__(self):
        self.playercontroller = PlayerController()
        self.tournamentcontroller = TournamentController()
        self.view = MenuView()
        self.quit = False

        self.current_menu = self.main_menu

    @property
    def main_menu(self):
        return [
            ("Menu Joueur", self.go_players_menu),
            ("Menu Tournoi", self.go_tournaments_menu),
        ]

    def executate(self):
        while not self.quit:
            action = self.navigate(self.current_menu)
            action()

    def navigate(self, menu):
        choicies = menu.copy()
        if self.current_menu != self.main_menu:
            choicies.append(("Retourner au menu principal", self.go_main_menu))
        choicies.append(("Quitter", self.go_quit))

        return self.view.ask_menu_choicies(choicies)

    def go_quit(self):
        self.quit = True

    def go_main_menu(self):
        self.current_menu = self.main_menu

    def go_players_menu(self):
        self.current_menu = [
            ("Ajouter un joueur", self.playercontroller.add_player),
            ("Voir la liste des joueurs", self.playercontroller.print_players),
        ]

    def go_tournaments_menu(self):
        self.current_menu = [
            ("Ajouter un tournoi", self.tournamentcontroller.add_tournament),
            ("Voir la liste des tournois", self.tournamentcontroller.print_tournaments),
            ("Selectionner un tournoi", self.tournamentcontroller.select_tournament)
        ]
