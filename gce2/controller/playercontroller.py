import gce2.manager.playermanager as playermanager
import gce2.view.playerview as playerview


class PlayerController:
    def __init__(self) -> None:
        self.view = playerview.PlayerView()
        self.manager = playermanager.PlayerManager()

    def add_player(self):
        data = self.view.ask_new_player()
        new_player = self.manager.post_player(data)
        print(f"Vous avez correctement ajouté le joueur suivant : \n {new_player}")

    def print_players(self):
        list_players = self.manager.get_players()
        self.view.list_players(list_players)
