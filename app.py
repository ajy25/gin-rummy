from flask import Flask, render_template, redirect, request, url_for
from src.game import Game
from random import randint

################################################################################
# Change MySQL database information in src/db_ops 
from src.db_ops import DBOperator
import mysql.connector


# SQL Server Information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sbds1234"
)
cursor = db.cursor(buffered=True)

db_name = 'test_sql'
cardtable_name = 'ginrummycards'
scoretable_name = 'ginrummyscores'
db_op = DBOperator(cursor, db_name=db_name, cardtable_name=cardtable_name, 
                   scoretable_name=scoretable_name)

games = dict() # key: gameID, value: Game

################################################################################
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def start_game():
    if request.method == 'POST':
        gameID = generate_id(cardtable_name)
        games[gameID] = Game(cursor, gameID, db_name, cardtable_name, 
                            scoretable_name)
        # return request.form.get("pvp")
        if request.form.get('pvp') == 'Play with a friend':
            return redirect(url_for("game_page_p1", gameID=gameID))
        elif request.form.get('computer') == 'Play with computer':
            return redirect(url_for("game_page_rummybot", gameID=gameID, 
                                    gamestate=0))
    return "none"

@app.route('/game/<gameID>/rummybot/<gamestate>')
def game_page_rummybot(gameID, gamestate):
    curr_game: Game = games[int(gameID)]
    ginfo = dict()
    ginfo['gameID'] = gameID
    ginfo['playernum'] = 1
    cards = curr_game.p1.view_cards()
    card_imgs = []
    for i in range(len(cards)):
        card_imgs.append(f'{cards[i].get_face_str()}_{cards[i].get_suit_str()}')
    ginfo['cards'] = card_imgs
    ginfo['deadwood'] = curr_game.p1.deadwood
    ginfo['selfscore'] = curr_game.p1_tally
    ginfo['oppscore'] = curr_game.p2_tally
    return render_template('play_rummybot.html', ginfo=ginfo)




@app.route('/game/<gameID>/<gametype>/discard', methods=['GET', 'POST'])
def player_decision(gameID, gametype):
    curr_game: Game = games[int(gameID)]

    if request.method == 'POST':
        out = []

        # return request.form.get("card1")

        for i in range(len(curr_game.p1.view_cards())):
            out.append(request.form.get(f"card{str(i)}form"))
            
            if request.form.get(f"card{i}form") == f"card{i}":
                if gametype == 'rummybot':
                    curr_game.turn_discard_by_idx(1, i)
                return redirect(url_for("game_page_rummybot", gameID=gameID, 
                        gamestate=1))

        return redirect(url_for("game_page_rummybot", gameID=gameID, 
                        gamestate=2))


@app.route('/game/<gameID>/p1vs')
def game_page_p1(gameID):
    curr_game: Game = games[int(gameID)]
    ginfo = dict()
    ginfo['playernum'] = 1
    cards = curr_game.p1.view_cards()

    
    for i in range(len(cards)):
        ginfo[f'card{i}face'] = cards[i].get_face_str()
        ginfo[f'card{i}suit'] = cards[i].get_suit_str()

    ginfo['selfscore'] = curr_game.p1_tally
    ginfo['oppscore'] = curr_game.p2_tally

    return render_template('play_versus.html', ginfo=ginfo)

@app.route('/game/<gameID>/p2vs')
def game_page_p2(gameID):
    curr_game: Game = games[int(gameID)]
    ginfo = dict()

    ginfo['playernum'] = 2
    cards = curr_game.p2.view_cards()
    for i in range(len(cards)):
        ginfo[f'card{i}face'] = cards[i].get_face_str()
        ginfo[f'card{i}suit'] = cards[i].get_suit_str()

    ginfo['selfscore'] = curr_game.p2_tally
    ginfo['oppscore'] = curr_game.p1_tally

    return render_template('play_versus.html', ginfo=ginfo)


################################################################################
def generate_id(table_name: str) -> int:
    count = 0
    while count < 100:
        gameID = randint(0, 10000)
        if not db_op.gameID_in_table(gameID, table_name):
            return gameID
        count += 1

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)

