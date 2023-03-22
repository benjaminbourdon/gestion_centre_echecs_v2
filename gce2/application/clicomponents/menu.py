from gce2.application.clicomponents.menuitems import MenuItems
import gce2.controller.commands as commands
from gce2.utils import _is_str


class Menu:
    AUTORIZED_KEYS = "1234567890ABCDEFGHIJKLMNORSTUVWXYZ"
    # Q and P reserved for Quit and ParentMenu actions

    def __init__(self, app, name, upper_menu=None) -> None:
        self.app = app
        self.name = name
        self.uppermenu = upper_menu

        self._submenuitems = {}
        self._commanditems = {}
        self._nbitem_unnamed = 0

    @property
    def uppermenu(self):
        return self._uppermenu

    @uppermenu.setter
    def uppermenu(self, upper_menu):
        if isinstance(upper_menu, Menu):
            self._uppermenu = upper_menu
        else:
            self._uppermenu = None

    @property
    def submenuitems(self):
        return self._submenuitems

    @property
    def commanditems(self):
        return self._commanditems

    def add_submenu(self, submenu):
        if isinstance(submenu, Menu):
            submenu.uppermenu = self
            new_submenuitem = MenuItems(
                text=submenu.name, command=commands.MofifyMenuCommand(menu=submenu, app=self.app)
            )
            self.submenuitems[self.next_key] = new_submenuitem

    @property
    def next_key(self):
        for char in self.AUTORIZED_KEYS:
            if char not in self.menuitems:
                return char

    @property
    def menuitems(self):
        all_items = self.commanditems | self.submenuitems
        if self.uppermenu is not None:
            all_items["P"] = MenuItems(
                text=f"Revenir à : {self.uppermenu.name}",
                command=commands.MofifyMenuCommand(menu=self.uppermenu, app=self.app),
            )
        all_items["Q"] = MenuItems(
            text="Quitter", command=commands.QuitCommand(app=self.app)
        )
        return all_items

    def add_commands(self, command, text="", request=None, template=None, key=None):
        if isinstance(command, commands.Command):
            if _is_str(text):
                text = str(text)
            else:
                self._nbitem_unnamed += 1
                text = f"Action #{self._nbitem_unnamed}"

            if key is None or key in self.menuitems:
                key = self.next_key

            if not callable(template):
                template = str

            self.commanditems[key] = MenuItems(text, command, request, template)

    def create_submenu(self, name):
        new_menu = Menu(self.app, name, self)
        self.add_submenu(new_menu)
        return new_menu

    def __str__(self) -> str:
        lines = [f"{self.name} :"]
        for key, menuitem in self.menuitems.items():
            lines.append(f"[{key}]\t{menuitem.text}")
        return "\n".join(lines)
