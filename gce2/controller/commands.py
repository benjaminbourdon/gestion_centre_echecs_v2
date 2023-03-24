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


class PostTournamentCommand(AppCommand):
    def executate(self):
        data = self.app.request
        try:
            new_tournament = self.app.managers["TournamentManager"].post_tournament(
                data
            )
        except Exception:
            raise Exception
        else:
            self.app.alert_msg = "Le tournoi a correctement été ajouté."
            return new_tournament


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
