from gce2.application.clicomponents.dynamicmenu import DynamicMenu
import gce2.controller.commands as commands
from gce2.exception.exception import CancelledActionException
import gce2.config as c


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
            self.add_commands(
                text="Voir la liste des tours",
                request=self.request_tournament_id,
                command=commands.GetTournamentCommand(self.app),
                template=self.app.view.template_list_rounds,
            )
            self.add_commands(
                text="Voir le détail d'un tour",
                request=self.request_round_id,
                command=commands.GetRoundCommand(self.app),
                template=self.app.view.template_resume_round,
            )
            self.add_commands(
                text="Ajouter des résultats de matchs au tour en cours",
                request=self.request_unknown_results,
                command=commands.PostGamesResultCommand(self.app),
                template=self.app.view.template_last_round,
            )
        else:
            if tournament.can_start():
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
            else:
                self.add_commands(
                    text="Ajouter un participant (un tournoi doit avoir un nombre pair de participants pour débuter)",
                    request=self.request_participant_id,
                    command=commands.AddParticipant(self.app),
                    template=self.app.view.template_list_participants,
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

    def request_round_id(self):
        tournament = self.linked_object
        list_rounds = tournament.rounds
        list_choicies = {i + 1: round.name for i, round in enumerate(list_rounds)}
        round_id = (
            self.app.view.select_info(list_choicies, "Tours finis ou entamés :") - 1
        )
        return {"tournament_id": self.linked_object.doc_id, "round_id": round_id}

    def request_unknown_results(self):
        tournament = self.linked_object
        current_round = tournament.last_round
        participants_names = {
            player.federal_id: f"{player.firstname} {player.lastname}"
            for player in tournament.participants
        }

        list_results = []
        for game in current_round.games:
            if c.SCORE["UNKNOW"] in {game[0][1], game[1][1]}:

                name_p1 = participants_names[game[0][0]]
                name_p2 = participants_names[game[1][0]]
                list_choicies = {
                    1: f"{name_p1} a gagné",
                    2: f"{name_p2} a gagné",
                    3: "Égalité",
                    4: "Je ne sais pas",
                }
                answer = self.app.view.select_info(
                    list_choicies,
                    f"{name_p1} contre {name_p2}:\nQuel est le résultat du match ?",
                )
                updated_game = game.copy()
                if answer == 4:
                    continue
                elif answer == 1:
                    updated_game[0][1] = c.SCORE["WIN"]
                    updated_game[1][1] = c.SCORE["LOSE"]
                elif answer == 2:
                    updated_game[0][1] = c.SCORE["LOSE"]
                    updated_game[1][1] = c.SCORE["WIN"]
                elif answer == 3:
                    updated_game[0][1] = c.SCORE["TIE"]
                    updated_game[1][1] = c.SCORE["TIE"]
                list_results.append(updated_game)
        return {
            "tournament_id": tournament.doc_id,
            "round_id": tournament.nb_rounds - 1,
            "games": list_results,
        }
