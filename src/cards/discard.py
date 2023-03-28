from .pile import Pile
from .card import Card

class Discard(Pile):
    '''DISCARD (extends PILE). 
    Discard pile. Only the top card can be seen and drawn. Behaves like a stack.
    '''
