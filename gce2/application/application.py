from abc import ABC

import gce2.controller.commands as commands
import gce2.exception.exception as e


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
                try:
                    data_fromrequest = request()
                except e.CancelledActionException:
                    self.alert_msg = "La saisie a éte annulée."
                    return
                else:
                    self.request.update(data_fromrequest)
            respond = command.executate()
            if hasattr(command, "log") and callable(command.log):
                command.log()
            if template is not None and callable(template):
                respond = template(respond)
            self.respond = respond
