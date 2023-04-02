import gce2.application.clicomponents.menu as m
import gce2.model.player as p
import gce2.config as c
import gce2.exception.exception as e
import gce2.model.tournament as t
import gce2.model.round as r
from gce2.utils import _is_int


class CliView:
    """Contains specific methods for CLI interraction : prints and requests

    Raises:
        CancelledActionException: raise when user stopped an input data request
    """

    NB_MAXTRY = 3

    FIELD_DESCRIPTION = {
        "lastname": "nom de famille",
        "firstname": "prénom",
        "federal_id": "numéro fédéral",
        "birthday": "date de naissance (JJ/MM/AAAA)",
        "tournament_id": "identifiant du tournoi",
        "name": "nom",
        "description": "description",
        "place": "lieu",
        "start_date": "date de début (JJ/MM/AAAA)",
        "end_date": "date de fin (JJ/MM/AAAA)",
        "max_round": "nombre de tour maximum",
    }

    CANCEL_WORLD = "!"

    """
    Generic methods
    """

    def clear(self) -> None:
        """Create blank lines to clear terminal screen"""
        print("\n" * 40)

    def separate(self) -> None:
        """Create a line to separate horizontaly"""
        print("___________________________")

    """
    Ask methods, return request as dict
    """

    def ask_menu_choice(self, menu: m.Menu) -> None:
        """Print menu and ask to choice an item from it

        Args:
            menu (Menu): navigated Menu object
        """
        print(menu)
        print("Votre choix : ", end="")
        return input().strip()

    def ask_info(
        self,
        list_field: list[str],
        text_intro: str = None,
        dict_default: dict[str, str] = None,
    ) -> dict[str, str]:
        """Generic method wich ask string data for a list of fields, one by one

        Args:
            list_field (List[str]): list of fields by name, use as key in return
            text_intro (str, optional): string print at first. Defaults to None.
            dict_default (Dict[str, str]): dict of default values for fiel item. Defaults to None.

        Raises:
            CancelledActionException: raise when user stopped its own request

        Returns:
            Dict[str, str]: field names as key and user inputs as values
        """
        if dict_default is None:
            dict_default = {}

        self.clear()
        if text_intro is not None:
            print(text_intro)
        print(f'(Taper "{self.CANCEL_WORLD}" à tout moment pour annuler la saisie)')

        data = {}
        for field in list_field:
            if field in self.FIELD_DESCRIPTION:
                text = self.FIELD_DESCRIPTION[field].capitalize()
            else:
                text = field.capitalize()
            if field in dict_default:
                text += f' ("{dict_default[field]}" par défaut)'

            answer = input(f"{text} > ").strip()
            if answer == self.CANCEL_WORLD:
                raise e.CancelledActionException
            elif answer == "":
                data[field] = dict_default[field]
            else:
                data[field] = answer
        return data

    def select_info(
        self, dict_choicies: dict[str | int, str], text_intro: str = None
    ) -> str | int | None:
        """Ask user to chose one valuem, by key values, among a list of possibilites

        Args:
            dict_choicies (Dict[str  |  int, str]): key among wich user have to chose
            and corresponding description as value.
            text_intro (str, optional): string print at first. Defaults to None.

        Raises:
            CancelledActionException: raise when user stopped its own request

        Returns:
            str | int | None: return string or integet key choose, same type as in dict_choicies argument.
            None if no valid answer after NB_MAXTRY tries.
        """
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
                raise e.CancelledActionException
            if answer in dict_choicies.keys():
                return answer
            if _is_int(answer) and int(answer) in dict_choicies.keys():
                return int(answer)
        raise e.CancelledActionException

    def ask_confirmation(self, text: str = "Êtes-vous sûr ?") -> None:
        """Ask a confirmation, raise an exception if user doesn't

        Args:
            text (str, optional): text print to ask confirmation. Defaults to "Êtes-vous sûr ?".

        Raises:
            CancelledActionException: raise if user doesn't confirm
        """
        answer = input(text + "(O / n)").strip()
        if answer in ["", "O"]:
            return None
        else:
            raise e.CancelledActionException

    # def ask_tournament_id(self) -> dict[str, str]:
    #     return self._ask_info(
    #         list_field=["tournament_id"],
    #         text_intro="Quel tournoi voulez-vous sélectionner ?",
    #     )

    def ask_new_tournament(self) -> dict[str, str]:
        """Ask user needed information to create a new tournament.

        Returns:
            Dict[str, str]: return dict with tournament core attributes
            as keys and user answer as values (or default for "max_round")
        """
        return self.ask_info(
            list_field=t.Tournament.CORE_ATTRIBUTES,
            text_intro="Merci de renseigner les informations suivantes",
            dict_default={"max_round": c.DEFAULT_NBROUND},
        )

    def ask_new_player(self) -> dict[str, str]:
        """Ask user needed information to create a new player.

        Returns:
            Dict[str, str]: return dict with player core attributes
            as keys and user answer as values.
        """
        return self.ask_info(
            p.Player.__slots__, "Merci de renseigner les informations suivantes"
        )

    def ask_player_id(self) -> dict[str, str]:
        """Ask a player federal id.

        Returns:
            Dict[str, str]: return dict with "federal_id" as key and user answer as value.
        """
        return self.ask_info(list_field=["federal_id"])

    """
    Templates
    """

    def template_list_players(self, player_list: list[p.Player]) -> str:
        lines = ["Voici la liste des joueurs enregistrés :"]
        lines.extend([str(player) for player in player_list])
        return "\n".join(lines)

    def template_resume_player(self, player: p.Player) -> str:
        text = ["Détail du joueur :"]
        for field in p.Player.__slots__:
            if field in self.FIELD_DESCRIPTION:
                field_name = self.FIELD_DESCRIPTION[field].capitalize()
            else:
                field_name = field.capitalize()
            field_value = getattr(player, field)
            text.append(f"{field_name:.<40} :\t{field_value}")
        return "\n".join(text)

    def template_list_tournaments(
        self, tournaments_list: list[t.Tournament]
    ) -> str:
        if tournaments_list is not None:
            lines = ["Voici la liste des tournois demandés :"]
            lines.extend(
                [
                    f"({tournament.doc_id:^3}) {tournament}"
                    for tournament in tournaments_list
                ]
            )
            return "\n".join(lines)
        else:
            return "Aucun tournoi ne correspond à votre demande."

    def template_resume_tournament(self, tournament: t.Tournament) -> str:
        if tournament is not None:
            return f"Le tournoi {tournament.name} se déroule du {tournament.start_date} au {tournament.end_date}"
        else:
            return "Aucun tournoi ne correspond à votre demande"

    def template_list_participants(self, tournament: t.Tournament) -> str:
        list_participants = tournament.participants

        if len(list_participants) > 0:
            lines = ["Les participants au tournoi sont :"]
            lines.extend([str(participant) for participant in list_participants])
            return "\n".join(lines)
        else:
            return "Ce tournoi n'a pas encore de participants."

    def template_last_round(self, tournament: t.Tournament) -> str:
        if tournament.nb_rounds == 0:
            return "Ce tournoi n'a pas encore de tour enregistré."
        else:
            last_round = tournament.last_round
            return f"{last_round.name} (tour {tournament.nb_rounds} sur {tournament.max_round})"

    def template_list_rounds(self, tournament: t.Tournament) -> str:
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

    def template_resume_round(self, round: r.Round) -> str:
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
