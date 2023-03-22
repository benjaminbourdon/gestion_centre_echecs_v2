from abc import ABC

import gce2.controller.commands as commands


class Application(ABC):
    def __init__(self, view, managers) -> None:
        self.respond = ""
        self.request = {}
        self.alert_msg = ""

        self.managers = managers
        self.view = view

    def executeCommand(self, command, request=None, template=None):
        if isinstance(command, commands.Command):
            if request is not None and callable(request):
                self.request.update(request())
            respond = command.executate()
            if hasattr(command, "log") and callable(command.log):
                command.log()
            if template is not None and callable(template):
                respond = template(respond)
            self.respond = respond
