import gce2.controller.commands as commands
from gce2.utils import _is_str


class MenuItems:
    def __init__(self, text, command, request=None, template=None) -> None:
        if _is_str(text):
            self.text = text
        else:
            self.text = ""

        if isinstance(command, commands.Command):
            self.command = command
        else:
            self.command = commands.DoNothingCommand()

        if callable(request):
            self.request = request
        else:
            self.request = None

        if callable(template):
            self.template = template
        else:
            self.template = None
