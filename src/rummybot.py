from .cards.hand import Hand
from .cards.card import Card
from .game import Game
import random
random.seed(3)

class RummyBot:
    '''RUMMYBOT

    A bot that plays Gin Rummy. Controls the Game class directly.
    '''

    # randomly move
    is_random: bool = None

    # info
    player_num: int = None
    game: Game = None
    hand: Hand = None                   # all information is provided by Hand

    # states for decision making; to be trained
    deadwood_multiplier: float = None       # to be modified in train_rummybot
    overlap_multiplier: float = None        # to be modified in train_rummybot
    mid_low_multiplier: float = None        # 

    def __init__(self, game: Game, player_num: int, is_random: bool = False) \
        -> None:
        
        self.is_random = is_random
        self.player_num = player_num
        self.game = game

        if player_num == 1:
            self.hand = self.game.p1
        elif player_num == 2:
            self.hand = self.game.p2
        else:
            raise Exception('Invalid input player_num.')

        self.deadwood_weight = random.random()
        self.overlap_weight = random.random()

    def move(self) -> None:
        if self.is_random == True:
            self.random_move()
        else:
            self.smart_move()


    def random_move(self) -> None:
        '''Randomly draw, and then randomly discard from deadwood cards.'''

        test = bool(random.randint(0, 1))

        if test:
            self.game.turn_draw(self.player_num, 'deck')
        else:
            self.game.turn_draw(self.player_num, 'discard')

        # STEP 1: DRAW
        idx = random.randint(0, len(self.hand.deadwood_cards) - 1)

        # STEP 2: DISCARD
        self.game.turn_discard(self.player_num, self.hand.deadwood_cards[idx])

        # STEP 3: TRY TO KNOCK
        self.game.turn_knock(self.player_num)
    
    def smart_move(self) -> None:
        '''Informed draw, then informed discard from deadwood cards.'''



