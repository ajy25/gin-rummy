import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/../src')


from cards.discard import Discard
from cards.deck import Deck
from cards.hand import Hand
from cards.card import Card
from cards.cardinfo import Value, Suit
import pytest
import random

def test_start():

    d = Deck()
    h1 = Hand()
    h2 = Hand()

    assert len(d) == 52
    assert h1.check() == False

    d.deal(h1, h2)

    assert len(d) == 32
    assert len(h1) == 10
    assert len(h2) == 10

    print(h1)
    h1.sort_cards(by='val')
    print(h1)

    d.repopulate()
    assert len(d) == 52

def test_remove():
    d = Deck()
    h1 = Hand()
    h2 = Hand()

    d.deal(h1, h2)
    
    assert len(h1) == 10
    h1.remove_card(h1.get_top().get_value(), h1.get_top().get_suit())
    assert len(h1) == 9

    assert len(h2) == 10
    assert h2.check() == True
    h2.remove_from_top()
    assert len(h2) == 9
    assert h2.check() == False

    h2.add(h1.get_top(), 4)
    assert len(h2) == 10
    assert h2.add(h1.get_top(), 10) == True
    assert len(h2) == 11
    assert h2.add(h1.get_top(), 12) == False

def test_score_info():
    h = Hand()

    # test duplicate
    h.add_to_top(Card(Value.TWO, Suit.CLUBS))
    h.add_to_top(Card(Value.THREE, Suit.CLUBS))
    h.add_to_top(Card(Value.FOUR, Suit.CLUBS))
    h.add_to_top(Card(Value.TWO, Suit.SPADES))
    h.add_to_top(Card(Value.TWO, Suit.DIAMONDS))

    h.add_to_top(Card(Value.ACE, Suit.HEARTS))

    h.add_to_top(Card(Value.TEN, Suit.HEARTS))
    h.add_to_top(Card(Value.JACK, Suit.HEARTS))
    h.add_to_top(Card(Value.QUEEN, Suit.HEARTS))
    h.add_to_top(Card(Value.KING, Suit.HEARTS))

    h.sort_cards()
    print(h)
    score, dw, melds, runs = h.score_info()
    print('score: ' + str(score))
    print('\nmelds: ')
    for meld in melds:
        print(meld)
    print('\nruns: ')
    for run in runs:
        print(run)
    print('\n\n\n')

    assert score == 5
    assert len(melds) == 0
    assert len(runs) == 7

    
    h.clear_all()
    h.add_to_top(Card(Value.NINE, Suit.HEARTS))
    h.add_to_top(Card(Value.TEN, Suit.HEARTS))
    h.add_to_top(Card(Value.JACK, Suit.HEARTS))
    h.add_to_top(Card(Value.QUEEN, Suit.HEARTS))
    h.add_to_top(Card(Value.KING, Suit.HEARTS))
    h.add_to_top(Card(Value.JACK, Suit.DIAMONDS))
    h.add_to_top(Card(Value.JACK, Suit.SPADES))
    h.add_to_top(Card(Value.QUEEN, Suit.DIAMONDS))
    h.add_to_top(Card(Value.QUEEN, Suit.SPADES))

    h.sort_cards()
    print(h)
    score, dw, melds, runs = h.score_info()
    print('score: ' + str(score))
    print('\ndeadwood cards: ')
    for card in dw:
        print(card)
    print('\nmelds: ')
    for meld in melds:
        print(meld)
    print('\nruns: ')
    for run in runs:
        print(run)
    print('\n\n\n')

    assert score == 29
    assert len(melds) == 6
    assert len(runs) == 0


if __name__ == '__main__':
    test_score_info()
