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
            return self.app.managers["TournamentManager"].get_tournament_by_id(
                tournament_id
            )
        else:
            return None

    def _construct_dynamic_menu(self):
        self.name = (
            f"Tournoi selectionné : {self.linked_object.name}\nActions disponibles"
        )
        self._commanditems = {}
        self.add_commands(
            text="Voir les participants",
            request=self.request_tournament_id,
            command=commands.GetParticipants(self.app),
            template=self.app.view.template_list_participants,
        )

    def request_tournament_id(self):
        return {"tournament_id": self.linked_object.doc_id}
