from .pile import Pile
from .card import Card
from .cardinfo import Value, Suit
import itertools
import copy

class Hand(Pile):
    '''HAND (extends PILE). 
    10 cards. Can reach 11 cards in play. All cards can be viewed by a player. 
    Any one card can be removed.
    '''

    deadwood = 0
    melds: list[Card] = []
    runs: list[Card] = []
    deadwood_cards: list[Card] = []
    
    melds_specific: list[list[Card]] = []
    runs_specific: list[list[Card]] = []

    def view_cards(self) -> list[Card]:
        '''Returns a shallow copy of the stack of cards.'''
        return copy.copy(self.stack)
    
    def check(self) -> bool:
        '''Ensures that the hand has 10 cards.'''
        if len(self.stack) == 10:
            return True
        else:
            return False
    
    def knockable(self) -> bool:
        '''Returns true if hand is <= 10 points deadwood.'''
        if self.deadwood > 10:
            return False
        else:
            return True

    def sort_cards(self, cards: list[Card] = None, by: str = 'val') -> \
        list[Card]:
        '''Sorts cards in the hand for easier viewing.

        Parameters:
            - self
            - card (optional): list of Cards to be sorted, self.stack by default
            - by (optional): String, either 'val' or 'suit', indicating how 
                the cards should be sorted. Default is by values. 

        Returns:
            - list of Cards, sorted
        '''
        def sort_by_suit(card: Card) -> float:
            '''Returns a float given a card, by suit priority.'''
            return card.suit.value + card.get_face_val() * 0.01

        def sort_by_val(card: Card) -> float:
            '''Returns a float given a card, by value priority.'''
            return card.get_face_val() + card.suit.value * 0.01

        if not cards:
            cards = self.stack

        if by == 'suit':
            cards.sort(key=sort_by_suit)
        elif by == 'val':
            cards.sort(key=sort_by_val)
        else:
            raise Exception('Invalid sort by value.')

        return cards

    def score_info(self, input_stack: list[Card] = None) -> tuple:
        '''Returns the integer deadwood value, list of melds, and list of runs.
        Also updates self.deadwood. Computes for best-case deadwood score.

        Parameters:
            - self

        Returns:
            - int: deadwood value
            - list[Card]: deadwood_cards
            - list[Card]: melds
            - list[Card]: runs
        '''
        if len(self.stack) == 0:
            return 0, [], [], []
        
        # just for typing reference
        sorted: list[Card] = []
        melds: list[list[Card]] = []
        runs: list[list[Card]] = []

        # make a shallow copy of the stack to maintain player's sorting 
        # preference; Card objects remain the same

        if not input_stack:
            sorted = copy.copy(self.stack)
        else:
            sorted = copy.copy(input_stack)
        
        # look for runs
        sorted = self.sort_cards(sorted, by='suit')

        runs_test: list[Card] = [sorted[0]]
        current_val = sorted[0].get_face_val()
        current_suit = sorted[0].get_suit_val()

        for i in range(1, len(sorted)):

            if sorted[i].get_face_val() == (current_val + 1) and \
                sorted[i].get_suit_val() == current_suit:
                runs_test.append(sorted[i])
            
            else:
                
                if len(runs_test) >= 3:
                    # shallow copy of runs_test
                    runs.append(copy.copy(runs_test))
                runs_test.clear()
                runs_test.append(sorted[i])
            
            current_val = sorted[i].get_face_val()
            current_suit = sorted[i].get_suit_val()

        # look for melds
        sorted = self.sort_cards(sorted, by='val')

        melds_test: list[Card] = [sorted[0]]
        current_val = sorted[0].get_face_val()

        for i in range(1, len(sorted)):

            if sorted[i].get_face_val() == current_val:

                melds_test.append(sorted[i])
            
            else:
                
                if len(melds_test) >= 3:
                    # shallow copy of melds_test
                    melds.append(copy.copy(melds_test))
                melds_test.clear()
                melds_test.append(sorted[i])
            
            current_val = sorted[i].get_face_val()
        
        # deal with overlap; goal is to return best-case deadwood score
        overlap: list[Card] = []
        for lst in melds:
            for card in lst:
                for lst in runs:
                    if card in lst:
                        overlap.append(card)
        
        m = len(overlap)

        # each card in overlap will be removed from melds or runs
        # there are 2^m possible ways of doing this, we will test each one
        # aim is to find the greatest possible loss in points

        tests = list(itertools.product([True, False], repeat=m))

        # True  -> remove from melds
        # False -> remove from runs

        # max points to beat
        max_extra = 0
        best_melds = []
        best_runs = []
        best_melds_specific = []
        best_runs_specific = []
        for test in tests:
            # make shallow copies of the melds and runs
            melds_copy = copy.copy(melds)
            runs_copy = copy.copy(runs)
            
            for i in range(m):
                if test[i]:
                    for lst in melds_copy:
                        if overlap[i] in lst:
                            melds_copy.remove(lst)
                else:
                    for lst in runs_copy:
                        if overlap[i] in lst:
                            runs_copy.remove(lst)
            
            test_extra = 0
            for lst in melds_copy:
                for card in lst:
                    test_extra += card.points
            for lst in runs_copy:
                for card in lst:
                    test_extra += card.points
            
            if test_extra > max_extra:
                max_extra = test_extra

                best_melds = []
                best_melds_specific = []
                for lst in melds_copy:
                    best_melds.extend(lst)
                    best_melds_specific.append(lst)

                best_runs = []
                best_runs_specific = []
                for lst in runs_copy:
                    best_runs.extend(lst)
                    best_runs_specific.append(lst)

        deadwood_cards = []

        all_points = 0
        for card in sorted:
            if (card not in best_melds) and (card not in best_runs):
                deadwood_cards.append(card)
            all_points += card.points

        deadwood = all_points - max_extra

        # only update self.deadwood if no input stack
        if not input_stack:
            self.deadwood = deadwood
            self.deadwood_cards = deadwood_cards
            self.melds = best_melds
            self.runs = best_runs
            self.melds_specific = best_melds_specific
            self.runs_specific = best_runs_specific
        
        return deadwood, deadwood_cards, best_melds, best_runs
    
    def remove_card(self, card: Card) -> Card:
        '''Removes a card given value and suit from the hand. Updates score.
        
        Parameters:
            - self
            - val: Value of Card to be removed
            - suit: Suit of Card to be removed

        Returns:
            - Card: Card to be removed if successful removal, None otherwise
        '''
        for i in range(len(self.stack)):
            target: Card = self.stack[i]
            if target.val == card.val and target.suit == card.suit:
                self.stack.remove(target)

                # update score info
                self.score_info()

                return target
        return None

    def remove_card_by_idx(self, idx: int) -> Card:
        '''Removes a card given position of card in stack. Updates score.
        
        Parameters:
            - self
            - idx: position of Card in stack to be removed
        
        Returns:
            - Card: Card to be removed if successful removal, None otherwise
        '''
        if idx in range(11):
            out = self.stack[idx]
            self.stack.pop(idx)

            # update score info
            self.score_info()

            return out
        return None
    
    def add_to_top_update_score(self, card: Card) -> None:
        '''Adds a card to the top of the pile. Then updates the score info.

        Parameters:
            - self
            - card: Card object to be added to pile
            
        Returns:
            - None
        '''
        self.stack.insert(0, card)
        self.score_info()

