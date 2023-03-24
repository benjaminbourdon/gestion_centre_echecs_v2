from gce2.application.cliapplication import CLIApplication
from gce2.manager.playermanager import PlayerManager
from gce2.manager.tournamentmanager import TournamentManager
from gce2.view.cliview import CliView


app = CLIApplication(
    view=CliView(),
    managers={
        "PlayerManager": PlayerManager(),
        "TournamentManager": TournamentManager(),
    },
)

app.run()
