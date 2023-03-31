from .cards.discard import Discard
from .cards.deck import Deck
from .cards.hand import Hand
from .cards.card import Card
from .cards.cardinfo import Suit, Value
import mysql.connector
import copy, random


class Game:
    '''GAME
    
    An instance of a Gin Rummy game between two players. This class handles 
    almost all important MySQL database interactions for front-end retrieval.
    '''

    cursor = None
    gameID: int = None
    p1: Hand = None
    p2: Hand = None
    deck: Deck = None
    discard: Discard = None
    db_name: str = None
    cardtable_name: str = None
    scoretable_name: str = None
    p1_tally: int = None
    p2_tally: int = None
    round_num: int = None
    round_complete: bool = None
    turn: int = None

    def __init__(self, cursor, id: int, db_name: str, \
        cardtable_name: str, scoretable_name: str):
        '''Deals cards to p1, p2. Then, discards top card from deck.'''

        self.cursor = cursor
        self.gameID = id
        self.db_name = db_name
        self.cardtable_name = cardtable_name
        self.scoretable_name = scoretable_name

        self.p1_tally = 0
        self.p2_tally = 0
        self.round_num = 1
        self.round_complete = False

        self.p1 = Hand()
        self.p2 = Hand()
        self.deck = Deck()          # shuffled 52 card deck
        self.discard = Discard()

        self.deck.deal(self.p1, self.p2)
        self.p1.sort_cards(by='suit')
        self.p2.sort_cards(by='suit')
        self.turn = random.randint(1, 2)

        # take one card from top of deck and move to discard pile
        self.discard.add_to_top(self.deck.draw())

        self.update_cardtable_from_piles()
        self.update_scoretable()
    
    def new_round(self) -> None:
        '''Shuffles and deals; wipes the discard. Increments round_num.'''
        self.round_complete = False

        self.round_num += 1
        self.discard.clear_all()
        self.p1.clear_all()
        self.p2.clear_all()
        self.deck.clear_all()
        self.deck.repopulate()
        self.deck.deal(self.p1, self.p2)
        self.p1.sort_cards(by='suit')
        self.p2.sort_cards(by='suit')

        # take one card from top of deck and move to discard pile
        self.discard.add_to_top(self.deck.draw())

        self.update_cardtable_from_piles()
        self.update_scoretable()
    
    def update_scoretable(self) -> None:
        '''Update the score table with appropriate scores and round number.'''

        self.cursor.execute('USE {}'.format(self.db_name))
        self.cursor.execute('DELETE FROM {} WHERE gameID={};'.format(\
            self.scoretable_name, str(self.gameID)))
        self.cursor.execute('INSERT INTO {}'.format(self.scoretable_name) +\
            '(gameID, p1, p2, roundnum) ' + \
            'VALUES ("{}", "{}", "{}", "{}");'.format(\
            str(self.gameID), str(self.p1_tally), str(self.p2_tally), \
            str(self.round_num)))

    def update_cardtable_from_piles(self) -> None:
        '''Remove all cards corresponding to game ID, and 
        re-add appropriately.'''

        # delete everything
        self.cursor.execute('USE {}'.format(self.db_name))
        self.cursor.execute('DELETE FROM {} WHERE gameID={};'.format(\
            self.cardtable_name, str(self.gameID)))
        
        # populate p1 info
        for i in range(len(self.p1.stack)):
            c = self.p1.stack[i]

            scoretype = ""
            if c in self.p1.deadwood_cards:
                scoretype = 'deadwood'
            elif c in self.p1.melds:
                scoretype = 'meld'
            elif c in self.p1.runs:
                scoretype = 'run'

            self.cursor.execute('USE {}'.format(self.db_name))
            self.cursor.execute('INSERT INTO {} '.format(self.cardtable_name) +\
                '(gameID, val, suit, pile, scoretype, stackorder) ' + \
                'VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(\
                str(self.gameID), c.get_face_str(), c.get_suit_str(), \
                'p1', scoretype, str(i)))
            
        # populate p2 info
        for i in range(len(self.p2.stack)):
            c = self.p2.stack[i]

            scoretype = ""
            if c in self.p2.deadwood_cards:
                scoretype = 'deadwood'
            elif c in self.p2.melds:
                scoretype = 'meld'
            elif c in self.p2.runs:
                scoretype = 'run'

            self.cursor.execute('USE {}'.format(self.db_name))
            self.cursor.execute('INSERT INTO {} '.format(self.cardtable_name) +\
                '(gameID, val, suit, pile, scoretype, stackorder) ' + \
                'VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(\
                str(self.gameID), c.get_face_str(), c.get_suit_str(), \
                'p2', scoretype, str(i)))

        # populate discard info
        for i in range(len(self.discard.stack)):
            c = self.discard.stack[i]
            self.cursor.execute('USE {}'.format(self.db_name))
            self.cursor.execute('INSERT INTO {} '.format(self.cardtable_name) +\
                '(gameID, val, suit, pile, stackorder) ' + \
                'VALUES ("{}", "{}", "{}", "{}", "{}");'.format(\
                str(self.gameID), c.get_face_str(), c.get_suit_str(), \
                'discard', str(i)))
        
        # populate deck info
        for i in range(len(self.deck.stack)):
            c = self.deck.stack[i]
            self.cursor.execute('USE {}'.format(self.db_name))
            self.cursor.execute('INSERT INTO {} '.format(self.cardtable_name) +\
                '(gameID, val, suit, pile, stackorder) ' + \
                'VALUES ("{}", "{}", "{}", "{}", "{}");'.format(\
                str(self.gameID), c.get_face_str(), c.get_suit_str(), \
                'deck', str(i)))

    def turn_draw(self, player_num: int, draw_option: str) -> None:
        '''Part of one turn of gin rummy. Player must draw a card.
        
        Parameters:
            - player_num: integer (either 1 or 2) representing player number
            - draw_option: string (either 'deck' or 'discard')

        Returns:
            - None
        '''

        if len(self.deck) == 0:
            self.tally_scores(player_num)
            self.round_complete = True
            return

        if player_num == 1:
            if self.turn != 1:
                raise Exception("It is not player 1's turn.")

            if draw_option == 'deck':
                self.p1.add_to_top(self.deck.draw())
            elif draw_option == 'discard':
                self.p1.add_to_top(self.discard.draw())
            else:
                raise Exception('Invalid input for draw_option.')
        elif player_num == 2:
            if self.turn != 2:
                raise Exception("It is not player 2's turn.")

            if draw_option == 'deck':
                self.p2.add_to_top(self.deck.draw())
            elif draw_option == 'discard':
                self.p2.add_to_top(self.discard.draw())
            else:
                raise Exception('Invalid input for draw_option.')
        else:
            raise Exception('Invalid input for player_num.')
        
        self.update_cardtable_from_piles()
    
    def turn_discard_by_idx(self, player_num: int, discard_idx: int) -> None:
        '''Part of one turn of gin rummy. After drawing a card, player must 
        discard a card.
        
        Parameters:
            - player_num: integer (either 1 or 2) representing player number
            - discard: int (position of card in the stack of the hand to be
                        removed)

        Returns:
            - None
        '''

        if player_num == 1:
            if self.turn != 1:
                raise Exception("It is not player 1's turn.")
            else:
                self.turn = 2
            if discard_idx in range(11):
                self.discard.add_to_top(self.p1.remove_card_by_idx(discard_idx))
            else:
                raise Exception('Length of stack not equal to 11.')
        elif player_num == 2:
            if self.turn != 2:
                raise Exception("It is not player 2's turn.")
            else:
                self.turn = 1
            if discard_idx in range(11):
                self.discard.add_to_top(self.p2.remove_card_by_idx(discard_idx))
            else:
                raise Exception('Length of stack not equal to 11.')
        else:
            raise Exception('Invalid input for player_num.')
        
        self.update_cardtable_from_piles()
    
    def turn_discard(self, player_num: int, card: Card) -> None:
        '''Part of one turn of gin rummy. After drawing a card, player must 
        discard a card.
        
        Parameters:
            - player_num: integer (either 1 or 2) representing player number
            - card: Card to get removed

        Returns:
            - None
        '''
        if player_num == 1:
            if self.turn != 1:
                raise Exception("It is not player 1's turn.")
            else:
                self.turn = 2
            self.discard.add_to_top(self.p1.remove_card(card))
        elif player_num == 2:
            if self.turn != 2:
                raise Exception("It is not player 2's turn.")
            else:
                self.turn = 1
            self.discard.add_to_top(self.p2.remove_card(card))
        else:
            raise Exception('Invalid input for player_num.')
        
        self.update_cardtable_from_piles()
    
    def turn_knock(self, player_num: int) -> bool:
        '''Part of one turn of gin rummy. A player may knock after their 
        deadwood is 10 or less. If knocking is possible, then scores are
        automatically tallied. A new round is NOT automatically started.
        
        Parameters:
            - player_num: integer (either 1 or 2) representing player number

        Returns:
            - bool: true if successful knock
        '''

        if player_num == 1:
            if self.p1.knockable():
                self.tally_scores(knocking_player_num=1)
                self.round_complete = True
                return True
            else:
                return False
        elif player_num == 2:
            if self.p2.knockable():
                self.tally_scores(knocking_player_num=2)
                self.round_complete = True
                return True
            else:
                return False
        else:
            return False

    def tally_scores(self, knocking_player_num: int) -> None:
        '''Score calculation process after a player has knocked.
        
        The opponent of the player who knocked has the opportunity to complete
        the melds and runs of the player who knocked with their cards.

        Parameters:
            - player_num: integer (either 1 or 2) representing player number
        '''

        if knocking_player_num == 1:
            print('\nPlayer 1 has knocked.\n')
        
            print('Player 1 Melds')
            for card in self.p1.melds:
                print(card)
            print('')

            print('Player 1 Runs')
            for card in self.p1.runs:
                print(card)
            print('')

            print('Player 1 Deadwood')
            for card in self.p1.deadwood_cards:
                print(card)
            print('')
        
            print('Player 2 Melds')
            for card in self.p2.melds:
                print(card)
            print('')

            print('Player 2 Runs')
            for card in self.p2.runs:
                print(card)
            print('')

            print('Player 2 Deadwood')
            for card in self.p2.deadwood_cards:
                print(card)
            print('')

            # deep copies of runs_specific
            knocking_player_runs_specific = copy.deepcopy(self.p1.runs_specific)

            runs_changed = True

            # each time a run has been modified, we need to recheck runs
            while runs_changed:

                runs_changed_local = False

                for lst in knocking_player_runs_specific:
                    suit_target: Suit = lst[0].suit
                    val_target_left: list[Value] = lst[0].get_face_val() - 1
                    val_target_right: list[Value] = lst[0].get_face_val() + 1

                    for card in self.p2.deadwood_cards:
                        if card.suit == suit_target:
                            if card.get_face_val() == val_target_left:
                                self.p1.add_to_top_update_score(\
                                    self.p2.remove_card(card))
                                lst.insert(0, card)
                                runs_changed_local = True
                            elif card.get_face_val() == val_target_right:
                                self.p1.add_to_top_update_score(\
                                    self.p2.remove_card(card))
                                lst.append(card)
                                runs_changed_local = True

                if runs_changed_local:
                    runs_changed = True
                else:
                    runs_changed = False
            
            for lst in self.p1.melds_specific:
                for card in self.p2.deadwood_cards:
                    if card.val == lst[0].val:
                        self.p1.add_to_top_update_score(\
                                    self.p2.remove_card(card))

            self.update_cardtable_from_piles()
            print(self)

            difference = abs(self.p2.deadwood - self.p1.deadwood)

            if self.p1.deadwood == 0:
                # case of gin
                self.p1_tally += 20 + difference
            else:
                # case of knock
                if self.p2.deadwood <= self.p1.deadwood:
                    self.p1_tally += 20 + difference
                else:
                    self.p2_tally += difference

        elif knocking_player_num == 2:
            print('\nPlayer 2 has knocked.\n')

            print('Player 1 Melds')
            for card in self.p1.melds:
                print(card)
            print('')

            print('Player 1 Runs')
            for card in self.p1.runs:
                print(card)
            print('')

            print('Player 1 Deadwood')
            for card in self.p1.deadwood_cards:
                print(card)
            print('')
        
            print('Player 2 Melds')
            for card in self.p2.melds:
                print(card)
            print('')

            print('Player 2 Runs')
            for card in self.p2.runs:
                print(card)
            print('')

            print('Player 2 Deadwood')
            for card in self.p2.deadwood_cards:
                print(card)
            print('')

            # deep copies of runs_specific
            knocking_player_runs_specific = copy.deepcopy(self.p2.runs_specific)

            runs_changed = True

            # each time a run has been modified, we need to recheck runs
            while runs_changed:

                runs_changed_local = False

                for lst in knocking_player_runs_specific:
                    suit_target: Suit = lst[0].suit
                    val_target_left: list[Value] = lst[0].get_face_val() - 1
                    val_target_right: list[Value] = lst[0].get_face_val() + 1

                    for card in self.p1.deadwood_cards:
                        if card.suit == suit_target:
                            if card.get_face_val() == val_target_left:
                                self.p2.add_to_top_update_score(\
                                    self.p1.remove_card(card))
                                lst.insert(0, card)
                                runs_changed_local = True
                            elif card.get_face_val() == val_target_right:
                                self.p2.add_to_top_update_score(\
                                    self.p1.remove_card(card))
                                lst.append(card)
                                runs_changed_local = True

                if runs_changed_local:
                    runs_changed = True
                else:
                    runs_changed = False
            
            for lst in self.p2.melds_specific:
                for card in self.p1.deadwood_cards:
                    if card.val == lst[0].val:
                        self.p1.add_to_top_update_score(\
                                    self.p1.remove_card(card))

            self.update_cardtable_from_piles()
            print(self)

            difference = abs(self.p1.deadwood - self.p2.deadwood)

            if self.p2.deadwood == 0:
                # case of gin
                self.p2_tally += 20 + difference
            else:
                # case of knock
                if self.p1.deadwood <= self.p2.deadwood:
                    self.p2_tally += 20 + difference
                else:
                    self.p1_tally += difference

        else:
            raise Exception('Invalid input for knocking_player_num.')
        
        self.update_scoretable()

    def __str__(self) -> str:
        '''String representation of cards'''
        out = 'ROUND NUMBER ' + str(self.round_num) + '\n'
        
        out += 'P1 CARDS | P1 SCORE: {} \n'.format(str(self.p1.deadwood)) \
            + str(self.p1) + '\n'
        out += 'P2 CARDS | P2 SCORE: {} \n'.format(str(self.p2.deadwood)) \
            + str(self.p2) + '\n'

        return out
        

















    







