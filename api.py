from flask import Flask, url_for, request
from gce2.manager.playermanager import PlayerManager
from gce2.manager.tournamentmanager import TournamentManager

ROOT = "http://127.0.0.1:5000"

app = Flask(__name__)


@app.get("/players")
def get_players():
    players = PlayerManager().get_players()
    return [
        player.to_dict()
        | {
            "_links": {
                "self": ROOT
                + url_for("get_player_by_id", id_fede=player.federal_id)
            }
        }
        for player in players
    ]


@app.post("/players")
def post_player():
    data = request.json
    print(data)
    player = PlayerManager().post_player(data)
    return player.to_dict() | {
        "_links": {
            "self": ROOT + url_for("get_player_by_id", id_fede=player.federal_id)
        }
    }


@app.get("/players/<id_fede>")
def get_player_by_id(id_fede):
    player = PlayerManager().get_player(id_fede)
    if player is None:
        return {}
    return player.to_dict()


@app.get("/tournaments")
def get_tournaments():
    tournaments = TournamentManager().get_tournaments()
    return [
        tournament.to_dict()
        | {
            "_links": {
                "self": ROOT
                + url_for("get_tournament_by_id", doc_id=tournament.doc_id)
            }
        }
        for tournament in tournaments
    ]


@app.get("/tournaments/<doc_id>")
def get_tournament_by_id(doc_id):
    tournament = TournamentManager().get_tournament_by_id(doc_id)
    if tournament is None:
        return {}
    return tournament.to_dict()
