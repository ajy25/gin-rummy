import random
from .cardinfo import Value, Suit
from .pile import Pile
from .hand import Hand
from .card import Card

class Deck(Pile):
    '''DECK (extends PILE). 
    Deck (standard 52-card). Only the top card can be seen and drawn. 
    Behaves like a stack.
    '''
    def __init__(self):
        Pile.__init__(self)
        self.repopulate()

    def repopulate(self) -> None:
        '''Populates self with a shuffled, standard 52-card deck.'''
        self.stack = []
        for v in Value:
            for s in Suit:
                self.add_to_top(Card(v, s))
        random.shuffle(self.stack)
    
    def deal(self, hand1: Hand, hand2: Hand) -> None:
        '''Deals cards to two Hands.

        Parameters:
            - self
            - hand1: Hand object, player 1
            - hand2: Hand object, player 2

        Returns:
            - None
        '''
        for i in range(10):
            hand1.add_to_top(self.draw())
            hand2.add_to_top(self.draw())
        hand1.score_info()
        hand2.score_info()
