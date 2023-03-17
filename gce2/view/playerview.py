from gce2.model.player import Player


class PlayerView:
    def ask_new_player(self):
        print("Merci de renseigner les informations suivantes")
        data = {}
        for field in Player.__slots__:
            data[field] = input(f"{field} > ")
        return data

    def list_players(self, player_list):
        print("Voici la liste des joueurs enregistrés :")
        for player in player_list:
            print(player)

    def select_player_id(self):
        return input("Quel est l'identifiant fédéral du joueur ?").strip()
