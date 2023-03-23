import gce2.exception.exception as exception


class CliView:

    FIELD_NAMES = {
        "lastname": "nom de famille",
        "firstname": "prénom",
        "federal_id": "numéro fédéral",
        "birthday": "date de naissance",
        "tournament_id": "identifiant du tournoi",
        "name": "nom",
        "description": "description",
        "place": "lieu",
        "start_date": "date de début",
        "end_date": "date de fin",
        "max_round": "nombre de tour maximum",
    }

    CANCEL_WORLD = "!"

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
        return self._ask_info(list_field=["federal_id"])

    def template_resume_player(self, player):
        return f"Détail du joueur :\n{str(player)}"

    def ask_new_player(self):
        from gce2.model.player import Player

        return self._ask_info(
            Player.__slots__, "Merci de renseigner les informations suivantes"
        )

    def template_list_tournaments(self, tournaments_list):
        if tournaments_list is not None:
            lines = ["Voici la liste des tournois demandés :"]
            lines.extend(
                [
                    f"[{tournament.doc_id}] {tournament}"
                    for tournament in tournaments_list
                ]
            )
            return "\n".join(lines)
        else:
            return "Aucun tournoi ne correspond à votre demande."

    def ask_tournament_id(self):
        return self._ask_info(list_field=["tournament_id"])

    def template_resume_tournament(self, tournament):
        if tournament is not None:
            return f"Le tournoi {tournament.name} se déroule du {tournament.start_date} au {tournament.end_date}"
        else:
            return "Aucun tournoi ne correspond à votre demande"

    def ask_new_tournament(self):
        from gce2.model.tournament import Tournament

        return self._ask_info(
            Tournament.CORE_ATTRIBUTES, "Merci de renseigner les informations suivantes"
        )

    def _ask_info(self, list_field, text_intro=None):
        self.clear()
        if text_intro is not None:
            print(text_intro)
            print(f'(Taper "{self.CANCEL_WORLD}" à tout moment pour annuler la saisie)')
        data = {}
        for field in list_field:
            if field in self.FIELD_NAMES:
                text = self.FIELD_NAMES[field].capitalize()
            else:
                text = field.capitalize()
            answer = input(f"{text} > ").strip()
            if answer == self.CANCEL_WORLD:
                raise exception.CancelledActionException
            else:
                data[field] = answer
        return data
