from abc import ABC, abstractmethod

import gce2.application.application as appmodul
import gce2.application.cliapplication as cliappmodul
import gce2.application.clicomponents.menu as menumodul
import gce2.exception.exception as exception


class Command(ABC):
    @abstractmethod
    def executate(self):
        raise NotImplementedError


class DoNothingCommand(Command):
    def executate(self):
        return None


class AppCommand(Command, ABC):
    def __init__(self, app, **kwargs) -> None:
        if isinstance(app, appmodul.Application):
            self.app = app
        else:
            raise Exception
        super().__init__(**kwargs)

    def get_request(self, key):
        try:
            requested = self.app.request[key]
        except KeyError:
            raise exception.InvalidRequestException
        else:
            return requested

    def get_allrequests(self):
        requested = self.app.request
        if isinstance(requested, dict):
            return requested
        else:
            raise exception.InvalidRequestException

    def get_tournament_fromrequest(self):
        manager = self.app.managers["TournamentManager"]
        tournament_id = self.get_request("tournament_id")
        tournament = manager.get_tournament_by_id(tournament_id)
        if tournament is None:
            self.app.alert_msg = (
                f"Le tournoi selectionné n'a pas éte trouvé (id={tournament_id})."
            )
            raise exception.InvalidRequestException
        return tournament

    def get_round_fromrequest(self):
        tournament = self.get_tournament_fromrequest()
        round_id = self.get_request("round_id")
        try:
            round = tournament.rounds[round_id]
        except IndexError:
            self.app.alert_msg = "Le tour selectionné n'a pas éte trouvé."
            raise exception.InvalidRequestException
        else:
            return round

    def orderby_fromrequest(self, list: list) -> list:
        try:
            orderby = self.get_request("orderby")
        except exception.InvalidRequestException:
            return list
        else:
            from operator import attrgetter

            try:
                sorted_list = sorted(list, key=attrgetter(orderby))
            except AttributeError:
                return list
            else:
                return sorted_list


class GetAllPlayersCommand(AppCommand):
    def executate(self):
        list_players = self.app.managers["PlayerManager"].get_players()
        return self.orderby_fromrequest(list_players)


class GetPlayerCommand(AppCommand):
    def executate(self):
        federal_id = self.get_request("federal_id")
        player = self.app.managers["PlayerManager"].get_player(federal_id)
        if player is None:
            self.app.alert_msg = (
                f"Aucun joueur ne correspond à l'identifiant {federal_id}."
            )
            raise exception.InvalidRequestException
        return player


class PostPlayerCommand(AppCommand):
    def executate(self):
        data = self.get_allrequests()
        new_player = self.app.managers["PlayerManager"].post_player(data)
        if new_player is None:
            self.app.alert_msg = "Le joueur n'a pas éte ajouté (donnée invalide)."
            raise exception.InvalidRequestException
        else:
            self.app.alert_msg = "Le joueur a correctement été ajouté."
            return new_player


class GetAllTournamentsCommand(AppCommand):
    def executate(self):
        return self.app.managers["TournamentManager"].get_tournaments()


class GetTournamentCommand(AppCommand):
    def executate(self):
        return self.get_tournament_fromrequest()


class GetParticipantsCommand(AppCommand):
    def executate(self):
        tournament = self.get_tournament_fromrequest()
        list_participants = tournament.participants
        return self.orderby_fromrequest(list_participants)


class AddParticipant(AppCommand):
    def executate(self):
        tournament_id = self.get_request("tournament_id")
        participant_id = self.get_request("federal_id")
        manager = self.app.managers["TournamentManager"]
        try:
            updated_tournament = manager.add_participant_in_tournament(
                tournament_id, participant_id
            )
        except AttributeError:
            self.app.alert_msg = "Le participant n'a pas éte ajouté."
            return None
        else:
            self.app.alert_msg = "Le participant a correctement éte ajouté."
            return updated_tournament.participants


class PostTournamentCommand(AppCommand):
    def executate(self):
        data = self.get_allrequests()
        manager = self.app.managers["TournamentManager"]
        new_tournament = manager.post_tournament(data)
        if new_tournament is None:
            self.app.alert_msg = "Le tournoi n'a pas éte ajouté (donnée invalide)."
            raise exception.InvalidRequestException
        else:
            self.app.alert_msg = "Le tournoi a correctement été ajouté."
            return new_tournament


class StartTournamentCommand(AppCommand):
    def executate(self):
        manager = self.app.managers["TournamentManager"]
        tournament = self.get_tournament_fromrequest()
        if not tournament.is_started() and len(tournament.participants) > 0:
            from gce2.model.round import Round

            first_round = Round(
                name="Tour 1",
                start_datetime=self.app.now,
                games=tournament.generate_random_games(),
            )
            try:
                tournament.add_round(first_round)
                manager.update_rounds(tournament)
            except exception.InsertRoundException:
                self.app.alert_msg = "Le premier tour n'a pas pu être créé."
                return None
            else:
                self.app.alert_msg = "Le tournoi a correctement été lancé."
                return tournament


class PostGamesResultCommand(AppCommand):
    def executate(self):
        round = self.get_round_fromrequest()

        games = self.get_request("games")
        try:
            for updating_game in games:
                round.game_update(updating_game)
        except exception.InsertRoundException:
            self.app.alert_msg = "Les résultats n'ont pas pu être enregistrés."
            return None
        else:
            self.app.managers["TournamentManager"].update_rounds(round.tournament)
            self.app.alert_msg = (
                "Les résultats des matchs existants ont éte pris en compte."
            )
            return round


class CloseRoundCommand(AppCommand):
    def executate(self):
        tournament = self.get_tournament_fromrequest()

        if tournament.last_round.allresults_known():
            tournament.last_round.end_datetime = self.app.now
            self.app.managers["TournamentManager"].update_rounds(tournament)

            if tournament.nb_rounds < tournament.max_round:
                self.app.alert_msg = (
                    "Le tour est cloturé, vous pouvez lancer le tour suivant."
                )
            else:
                self.app.alert_msg = (
                    "Le tournoi est cloturé (tous les tours sont finis)."
                )
            return tournament.last_round
        else:
            self.app.alert_msg = (
                "Le tour ne peut pas être cloturé (des résultats ne sont pas connus)."
            )
            return None


class StartNextRoundCommand(AppCommand):
    def executate(self):
        from gce2.model.round import Round

        tournament = self.get_tournament_fromrequest()
        nb_next_round = tournament.nb_rounds + 1
        next_round = Round(
            name=f"Tour {nb_next_round}",
            start_datetime=self.app.now,
            games=tournament.generate_ranked_games(),
        )

        try:
            tournament.add_round(next_round)
            self.app.managers["TournamentManager"].update_rounds(tournament)
        except exception.InsertRoundException:
            self.app.alert_msg = "Le tour suivant n'a pas pu être créé."
            return None
        else:
            self.app.alert_msg = "Le tour suivant a correctement été créé."
            return tournament.last_round


class GetRoundCommand(AppCommand):
    def executate(self):
        return self.get_round_fromrequest()


class CLIAppCommand(AppCommand, ABC):
    def __init__(self, app, **kwargs) -> None:
        if not isinstance(app, cliappmodul.CLIApplication):
            raise Exception
        super().__init__(app, **kwargs)


class MofifyMenuCommand(CLIAppCommand):
    def __init__(self, menu, **kwargs) -> None:
        if isinstance(menu, menumodul.Menu):
            self.menu = menu
        super().__init__(**kwargs)

    def executate(self):
        if hasattr(self, "menu"):
            self.app.transition_to(self.menu)


class LaunchDynamicMenuCommand(CLIAppCommand):
    def __init__(self, class_menu, **kwargs) -> None:
        from gce2.application.clicomponents.dynamicmenu import DynamicMenu

        if issubclass(class_menu, DynamicMenu):
            self.class_menu = class_menu
        super().__init__(**kwargs)

    def executate(self):
        try:
            dynamic_menu = self.class_menu(
                app=self.app, name="Menu dynamique", upper_menu=self.app.menu
            )
        except exception.NotInstanciatedMenuException:
            self.app.alert_msg = "Le menu n'a pas pu être instancié."
        else:
            self.app.transition_to(dynamic_menu)


class QuitCommand(CLIAppCommand):
    def executate(self):
        self.app.quit()
        return ""
