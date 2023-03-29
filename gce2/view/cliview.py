import gce2.exception.exception as exception
from gce2.utils import _is_int
import gce2.config as c


class CliView:

    NB_MAXTRY = 3

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
                    f"({tournament.doc_id}) {tournament}"
                    for tournament in tournaments_list
                ]
            )
            return "\n".join(lines)
        else:
            return "Aucun tournoi ne correspond à votre demande."

    def ask_tournament_id(self):
        return self._ask_info(
            list_field=["tournament_id"],
            text_intro="Quel tournoi voulez-vous sélectionner ?",
        )

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

    def select_info(self, dict_choicies, text_intro=None):
        self.clear()
        if text_intro is not None:
            print(text_intro)
        print(f'(Taper "{self.CANCEL_WORLD}" à tout moment pour annuler la saisie)')
        for key, values in dict_choicies.items():
            print(f"[{key}]\t{values}")

        for nb_try in range(self.NB_MAXTRY):
            if nb_try > 0:
                print(
                    f"Saisie incorrecte. {nb_try+1}e essai ({self.NB_MAXTRY} essais maximum)"
                )
            answer = input("Votre choix (sensible à la case) : ").strip()
            if answer == self.CANCEL_WORLD:
                raise exception.CancelledActionException
            if answer in dict_choicies.keys():
                return answer
            if _is_int(answer) and int(answer) in dict_choicies.keys():
                return int(answer)
        return None

    def template_list_participants(self, tournament):
        list_participants = tournament.participants

        if len(list_participants) > 0:
            lines = ["Les participants au tournoi sont :"]
            lines.extend([str(participant) for participant in list_participants])
            return "\n".join(lines)
        else:
            return "Ce tournoi n'a pas encore de participants."

    def ask_confirmation(self, text="Êtes-vous sûr ?"):
        answer = input(text + "(O / n)").strip()
        if answer in ["", "O"]:
            return None
        else:
            raise exception.CancelledActionException

    def template_last_round(self, tournament):
        last_round = tournament.last_round
        return f"{last_round.name} (tour {len(tournament.rounds)} sur {tournament.max_round})"

    def template_list_rounds(self, tournament):
        if tournament.nb_rounds == 0:
            return "Ce tournoi n'a pas encore de tour enregistré."

        rounds = tournament.rounds
        lines = [f"Liste des tours :\n(Tournoi en {tournament.max_round} tours)"]
        for round in rounds:
            if round.iscompleted():
                statut = "fini"
            else:
                statut = "en cours"
            lines.append(f"> {round.name} ({statut})")
        return "\n".join(lines)

    def template_resume_round(self, round):
        if round.iscompleted():
            intro = f"{round.name} (fini) s'est déroulé du {round.start_datetime} au {round.end_datetime}"
        else:
            intro = f"{round.name} (en cours) a débuté le {round.start_datetime}"

        participants_name = {
            participant.federal_id: participant.fullname
            for participant in round.tournament.participants
        }
        result = []
        for game in round.games:
            player1 = participants_name[game[0][0]]
            player2 = participants_name[game[1][0]]
            text = f" {player1:_<30} contre {player2:_>30}\t:\t"

            if game[0][1] == c.SCORE["WIN"] and game[1][1] == c.SCORE["LOSE"]:
                text += f"{player1} a gagné"
            elif game[0][1] == c.SCORE["LOSE"] and game[1][1] == c.SCORE["WIN"]:
                text += f"{player2} a gagné"
            elif game[0][1] == c.SCORE["TIE"] and game[1][1] == c.SCORE["TIE"]:
                text += "égalité"
            else:
                text += "résultat non connu"
            result.append(text)

        return intro + "\n" + "\n".join(result)
