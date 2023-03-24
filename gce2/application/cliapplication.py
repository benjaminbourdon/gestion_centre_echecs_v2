from gce2.application.application import Application
from gce2.application.clicomponents.menu import Menu
from gce2.application.clicomponents.tournamentdynamicmenu import TournamentDynamicMenu
import gce2.controller.commands as commands


# State dessign pattern : CLIApplication is a Context and Menu are states
class CLIApplication(Application):
    def __init__(self, view, managers) -> None:
        super().__init__(view, managers)
        self._keep_running = True
        self.construct_menu()

    def run(self):
        while self.keep_running:
            selected_key = self.refresh_screen()

            selected_key = str(selected_key).upper()
            if len(selected_key) == 1 and selected_key in self.menu.menuitems:
                selected_item = self.menu.menuitems[selected_key]
                self.executeCommand(
                    command=selected_item.command,
                    request=selected_item.request,
                    template=selected_item.template,
                )
            else:
                self.alert_msg = (
                    "/!\\ Vous devez indiquer une entrée valide. Ré-essayer."
                )

    @property
    def menu(self):
        return self._menu

    @property
    def keep_running(self):
        return self._keep_running

    def quit(self):
        self._keep_running = False

    def transition_to(self, menu):
        if isinstance(menu, Menu):
            self._menu = menu

    def refresh_screen(self):
        self.view.clear()
        if self.respond is not None:
            print(self.respond)
            self.view.separate()
        if self.alert_msg != "":
            print(self.alert_msg)
            self.alert_msg = ""
            self.view.separate()
        return self.view.ask_menu_choice(self.menu)

    def construct_menu(self):
        main_menu = Menu(self, "Menu Principal")
        player_menu = main_menu.create_submenu("Menu Joueur")
        player_menu.add_commands(
            text="Voir tous les joueurs",
            command=commands.GetAllPlayersCommand(self),
            template=self.view.template_list_players,
        )
        player_menu.add_commands(
            text="Sélectionner un joueur",
            request=self.view.ask_player_id,
            command=commands.GetPlayerCommand(self),
            template=self.view.template_resume_player,
        )
        player_menu.add_commands(
            text="Ajouter un joueur",
            request=self.view.ask_new_player,
            command=commands.PostPlayerCommand(self),
            template=self.view.template_resume_player,
        )

        tournament_menu = main_menu.create_submenu("Menu Tournoi")
        tournament_menu.add_commands(
            text="Voir tous les tournois",
            command=commands.GetAllTournamentsCommand(self),
            template=self.view.template_list_tournaments,
        )
        # tournament_menu.add_commands(
        #     text="Sélectionner un tournoi",
        #     request=self.view.ask_tournament_id,
        #     command=commands.GetTournamentCommand(self),
        #     template=self.view.template_resume_tournament,
        # )
        tournament_menu.add_commands(
            text="Ajouter un tournoi",
            request=self.view.ask_new_tournament,
            command=commands.PostTournamentCommand(self),
            template=self.view.template_resume_tournament,
        )
        tournament_menu.add_commands(
            text="Sélectionner un tournoi",
            command=commands.LaunchDynamicMenuCommand(class_menu=TournamentDynamicMenu, app=self)
        )
        self.transition_to(main_menu)
