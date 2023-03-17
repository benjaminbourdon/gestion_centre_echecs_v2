import gce2.manager.playermanager as playermanager
import gce2.view.playerview as playerview
import gce2.utils as utils


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

    def select_player(self):
        self.print_players()
        player_id = self.view.select_player_id()
        if utils._is_str(player_id):
            selected_player = self.manager.get_player(player_id)
            if selected_player is not None:
                return selected_player
            else:
                raise BaseException
        else:
            raise BaseException
