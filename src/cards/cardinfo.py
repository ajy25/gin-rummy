from enum import Enum

class Suit(Enum):
    '''Enum for card suits.'''
    CLUBS = 1
    SPADES = 2
    HEARTS = 3
    DIAMONDS = 4

class Value(Enum):
    '''Enum for card values.'''
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13