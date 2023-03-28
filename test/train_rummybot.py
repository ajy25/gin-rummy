import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/../')

from src.rummybot import RummyBot
from src.game import Game
from src import db_ops

class TrainRummyBot:

    db_name, cardtable_name, scoretable_name = None, None, None

    g: Game = None
    rb1: RummyBot = None        # controls p1
    rb2: RummyBot = None        # controls p2

    def __init__(self):
        self.db_name, self.cardtable_name, self.scoretable_name = \
            'test_sql', 'ginrummycards', 'ginrummyscores'

        db_ops.setup(self.db_name, self.cardtable_name, self.scoretable_name)

        self.g = Game(db_ops.cursor, 20, \
            self.db_name, self.cardtable_name, self.scoretable_name)

        self.rb1 = RummyBot(self.g, 1, True)
        self.rb2 = RummyBot(self.g, 2, True)

    def simulate_one_round(self):
        '''Plays a round of Gin Rummy.'''

        starting_player: RummyBot = None
        opponent: RummyBot = None

        # players alternate starting first
        if self.g.round_num % 2 == 1:
            starting_player = self.rb1
            opponent = self.rb2
        else:
            starting_player = self.rb2
            opponent = self.rb1

        while True:

            if not self.g.round_complete:
                starting_player.move()
            else:
                break
            
            if not self.g.round_complete:
                opponent.move()
            else:
                break
        
        # db_ops.print_rows(self.db_name, self.cardtable_name)
        db_ops.print_rows(self.db_name, self.scoretable_name)
        self.g.new_round()
    
    def simulate_complete_game(self): 
        '''Plays an entire game of Gin Rummy.'''

        while self.g.p1_tally < 100 and self.g.p2_tally < 100:
            self.simulate_one_round()

if __name__ == '__main__':
    t = TrainRummyBot()

    # t.simulate_one_round()
    # t.simulate_one_round()

    t.simulate_complete_game()



