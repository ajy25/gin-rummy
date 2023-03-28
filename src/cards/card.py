from .cardinfo import Suit, Value

class Card:
    '''CARD. 
    A playing card with a face value and a suit classification.
    '''

    val = None
    suit = None
    points = None

    def __init__(self, val: Value, suit: Suit):
        self.val = val
        self.suit = suit
        if val.value > 10:
            self.points = 10
        else:
            self.points = val.value
    
    def get_face_val(self) -> int:
        '''Returns integer face value.'''
        return self.val.value
    
    def get_suit_val(self) -> int:
        '''Returns integer suit value.'''
        return self.suit.value

    def get_face_str(self) -> str:
        '''Returns string face value.'''
        return str(self.val.name)
    
    def get_suit_str(self) -> str:
        '''Returns string face value.'''
        return str(self.suit.name)
    
    def __str__(self) -> str:
        '''String representation.'''
        out =  self.val.name + '  \tof\t' + self.suit.name + \
            ':   \t' + str(self.points) + '\t points'
        return out
