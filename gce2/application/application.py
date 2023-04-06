from abc import ABC

from datetime import datetime

import gce2.controller.commands as commands
import gce2.exception.exception as exception
import gce2.config as config


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
                except exception.CancelledActionException:
                    self.alert_msg = "La saisie a éte annulée."
                    return
                else:
                    self.request.update(data_fromrequest)

            try:
                respond = command.executate()
            except exception.InvalidRequestException:
                if self.alert_msg == "":
                    self.alert_msg = "La requête est incorrecte. L'action n'a pas pu être réalisée."
                return

            if template is not None and callable(template):
                respond = template(respond)
            self.respond = respond

    @property
    def now(self):
        return datetime.now().strftime(config.DATETIME_FORMAT)

    @property
    def today(self):
        return datetime.now().strftime(config.DATE_FORMAT)
