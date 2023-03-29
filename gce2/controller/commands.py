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


class GetAllPlayersCommand(AppCommand):
    def executate(self):
        return self.app.managers["PlayerManager"].get_players()


class GetPlayerCommand(AppCommand):
    def executate(self):
        federal_id = self.app.request["federal_id"]
        return self.app.managers["PlayerManager"].get_player(federal_id)


class PostPlayerCommand(AppCommand):
    def executate(self):
        data = self.app.request
        try:
            new_player = self.app.managers["PlayerManager"].post_player(data)
        except Exception:
            raise Exception
        else:
            self.app.alert_msg = "Le joueur a correctement été ajouté."
            return new_player


class GetAllTournamentsCommand(AppCommand):
    def executate(self):
        return self.app.managers["TournamentManager"].get_tournaments()


class GetTournamentCommand(AppCommand):
    def executate(self):
        tournament_id = self.app.request["tournament_id"]
        return self.app.managers["TournamentManager"].get_tournament_by_id(
            tournament_id
        )


class GetParticipants(AppCommand):
    def executate(self):
        tournament_id = self.app.request["tournament_id"]
        return (
            self.app.managers["TournamentManager"]
            .get_tournament_by_id(tournament_id)
            .participants
        )


class AddParticipant(AppCommand):
    def executate(self):
        tournament_id = self.app.request["tournament_id"]
        participant_id = self.app.request["federal_id"]
        manager = self.app.managers["TournamentManager"]
        try:
            updated_tournament = manager.add_participant_in_tournament(
                tournament_id, participant_id
            )
        except Exception:
            raise Exception
        else:
            self.app.alert_msg = "Le participant a correctement éte ajouté."
            return updated_tournament


class PostTournamentCommand(AppCommand):
    def executate(self):
        data = self.app.request
        manager = self.app.managers["TournamentManager"]
        try:
            new_tournament = manager.post_tournament(data)
        except Exception:
            raise Exception
        else:
            self.app.alert_msg = "Le tournoi a correctement été ajouté."
            return new_tournament


class StartTournamentCommand(AppCommand):
    def executate(self):
        tournament_id = self.app.request["tournament_id"]
        manager = self.app.managers["TournamentManager"]
        tournament = manager.get_tournament_by_id(tournament_id)
        if not tournament.is_started() and len(tournament.participants) > 0:
            from datetime import date
            from gce2.model.round import Round

            date_today = date.today().strftime("%d/%m/%y")
            first_round = Round(
                {
                    "name": "Tour 1",
                    "start_datetime": date_today,
                    "games": tournament.generate_random_games(),
                }
            )
            try:
                tournament.add_round(first_round)
                manager.update_rounds(tournament)
            except exception.InsertRoundException:
                self.app.alert_msg = "Le premier tour n'a pas pu être crée."
                return None
            else:
                self.app.alert_msg = "Le tournoi a correctement été lancé."
                return tournament


class GetRoundCommand(AppCommand):
    def executate(self):
        manager = self.app.managers["TournamentManager"]
        tournament_id = self.app.request["tournament_id"]
        round_id = self.app.request["round_id"]

        tournament = manager.get_tournament_by_id(tournament_id)
        round = tournament.rounds[round_id]
        return round


# class PostGameResultCommand(AppCommand):
#     def executate(self):
#         manager = self.app.managers["TournamentManager"]
#         tournament_id = self.app.request["tournament_id"]
#         round_id = self.app.request["round_id"]
#         game_result = self.app.request["game_result"]


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
