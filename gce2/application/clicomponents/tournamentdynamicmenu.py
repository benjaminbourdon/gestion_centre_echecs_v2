from gce2.application.clicomponents.dynamicmenu import DynamicMenu
import gce2.controller.commands as commands
from gce2.exception.exception import CancelledActionException


class TournamentDynamicMenu(DynamicMenu):
    def _select_linked_object(self):
        list_tournament = self.app.managers["TournamentManager"].get_tournaments()
        list_choicies = {
            tournament.doc_id: tournament.name for tournament in list_tournament
        }
        try:
            tournament_id = self.app.view.select_info(
                list_choicies, text_intro="À quel tournoi voulez-vous accéder ?"
            )
        except CancelledActionException:
            tournament_id = None

        if tournament_id is not None:
            return (
                self.app.managers["TournamentManager"].get_tournament_by_id,
                tournament_id,
            )
        else:
            return None

    def _construct_dynamic_menu(self):
        tournament = self.linked_object

        self.name = (
            f"Tournoi selectionné : {self.linked_object.name}\nActions disponibles"
        )
        self._commanditems = {}
        self.add_commands(
            text="Voir les participants",
            request=self.request_tournament_id,
            command=commands.GetTournamentCommand(self.app),
            template=self.app.view.template_list_participants,
        )
        if tournament.is_started():
            pass
        else:
            self.add_commands(
                text="Ajouter un participant",
                request=self.request_participant_id,
                command=commands.AddParticipant(self.app),
                template=self.app.view.template_list_participants,
            )
            self.add_commands(
                text="Commencer le tournoi",
                request=self.confirm_request_tournament_id,
                command=commands.StartTournamentCommand(self.app),
                template=self.app.view.template_last_round,
            )

    def request_tournament_id(self):
        return {"tournament_id": self.linked_object.doc_id}

    def confirm_request_tournament_id(self):
        self.app.view.ask_confirmation()
        return self.request_tournament_id()

    def request_participant_id(self):
        list_players = self.app.managers["PlayerManager"].get_players()
        tournament_id = self.linked_object.doc_id
        tournament = self.app.managers["TournamentManager"].get_tournament_by_id(
            tournament_id
        )
        participants_id = [
            participant.federal_id for participant in tournament.participants
        ]
        list_choicies = {
            player.federal_id: f"{player.firstname} {player.lastname}"
            for player in list_players
            if player.federal_id not in participants_id
        }

        federal_id = self.app.view.select_info(
            list_choicies, "Joueurs ne participant pas encore :"
        )
        return {"tournament_id": self.linked_object.doc_id, "federal_id": federal_id}
