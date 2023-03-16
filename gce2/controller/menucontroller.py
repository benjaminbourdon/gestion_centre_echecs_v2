from gce2.controller.playercontroller import PlayerController
from gce2.view.menuview import MenuView


class MenuController:
    def __init__(self):
        self.playercontroller = PlayerController()
        self.view = MenuView()
        self.quit = False

        self.current_menu = self.main_menu

    @property
    def main_menu(self):
        return [("Menu Joueur", self.go_player_menu)]

    def executate(self):
        while not self.quit:
            action = self.navigate(self.current_menu)
            action()

    def navigate(self, menu):
        choicies = menu.copy()
        if self.current_menu != self.main_menu:
            choicies.append(("Retourner au menu principal", self.go_main_menu))
        choicies.append(("Quitter", self.go_quit))

        while True:
            answer = self.view.ask_choice(choicies)

            try:
                answer = int(answer)
                try:
                    action = choicies[answer][1]
                    return action
                except IndexError:
                    print("Le chiffre indiqué n'est pas valide. Ré-essayer.")
            except ValueError:
                print("Vous devez indiquer un numéro. Ré-essayer.")

    def go_quit(self):
        self.quit = True

    def go_main_menu(self):
        self.current_menu = self.main_menu

    def go_player_menu(self):
        self.current_menu = [
            ("Ajouter un joueur", self.playercontroller.add_player),
            ("Voir la liste des joueurs", self.playercontroller.print_players),
        ]
