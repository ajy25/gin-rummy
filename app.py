from flask import Flask

from src.game import Game
from src.db_ops import *

app = Flask(__name__)


@app.route('/')
def welcome():
    header = '<h1>Gin Rummy</h1>'
    start_game = f'<p><a href="game/{id}">Click me!</a></p>'

    return 

if __name__ == '__main__':
    app.run(debug=True)

