from flask import Flask, jsonify, request, url_for
from flask_swagger import swagger

from gce2.manager.playermanager import PlayerManager
from gce2.manager.tournamentmanager import TournamentManager

ROOT = "http://127.0.0.1:5000"


def modify_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


app = Flask(__name__)
app.after_request(modify_header)


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag["info"]["version"] = "1.0"
    swag["info"]["title"] = "GCE2 API"

    return jsonify(swag)


@app.errorhandler(ValueError)
def request_invalid_value(error):
    return str(error), 405


@app.get("/players")
def get_players():
    """
    Return list of players
    ---
    tags:
        - players
    produces:
        - application/json
    responses:
        '200':
            description: Players accessed.
    """
    players = PlayerManager().get_players()
    return [
        player.to_dict()
        # | {
        #     "_links": {
        #         "self": ROOT + url_for("get_player_by_id", id_fede=player.federal_id)
        #     }
        # }
        for player in players
    ]


@app.post("/players")
def post_player():
    """
    Add a player
    ---
    tags:
        - players
    parameters:
        -   in: body
            name: body
            schema:
                id: Player
                required:
                    - federal_id
                    - birthday
                    - firstname
                    - lastname
                properties:
                    federal_id:
                        type: string
                        example: AB12345
                    birthday:
                        type: string
                        example: 03/05/1997
                    firstname:
                        type: string
                        example: Annie
                    lastname:
                        type: string
                        example: Dupond
    responses:
        '200':
            description: Player added.
        '405':
            description: Federal ID already exist
    """
    data = request.json
    player = PlayerManager().post_player(data)
    return player.to_dict()
    # | {
    # "_links": {
    #     "self": ROOT + url_for("get_player_by_id", id_fede=player.federal_id)
    # }}


@app.get("/players/<federal_id>")
def get_player_by_id(federal_id):
    """
    Return a player based on federal id
    ---
    tags:
        -   players
    produces:
        -   application/json
    parameters:
        -   in: path
            name: federal_id
            description: player's federal id
            required: true
    responses:
        '200':
            description: Player accessed.
    """
    player = PlayerManager().get_player(federal_id)
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
                "self": ROOT + url_for("get_tournament_by_id", doc_id=tournament.doc_id)
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
