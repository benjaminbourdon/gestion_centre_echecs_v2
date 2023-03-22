class CliView:

    TRADUCTION = {"lastname": "nom de famille"}

    def clear(self):
        print("\n" * 40)

    def separate(self):
        print("___________________________")

    def ask_menu_choice(self, menu):
        print(menu)
        print("Votre choix : ", end="")
        return input().strip()

    def template_list_players(self, player_list):
        lines = ["Voici la liste des joueurs enregistrés :"]
        lines.extend([str(player) for player in player_list])
        return "\n".join(lines)

    def ask_player_id(self):
        federal_id = input("Quel est l'identifiant fédéral du joueur ? ").strip()
        return {"federal_id": str(federal_id)}

    def template_resume_player(self, player):
        return f"Détail du joueur :\n{str(player)}"

    def ask_new_player(self):
        print("Merci de renseigner les informations suivantes")
        data = {}
        from gce2.model.player import Player

        for field in Player.__slots__:
            if field in self.TRADUCTION:
                text = self.TRADUCTION[field].capitalize()
            else:
                text = field.capitalize()
            data[field] = input(f"{text} > ")
        return data
