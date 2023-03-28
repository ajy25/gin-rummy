from .card import Card
import mysql.connector

class Pile:

    stack: list[Card] = None

    def __init__(self):
        self.stack = []
    
    def add_to_top(self, card: Card) -> None:
        '''Adds a card to the top of the pile. 

        Parameters:
            - self
            - card: Card object to be added to pile
            
        Returns:
            - None
        '''
        self.stack.insert(0, card)
    
    def add(self, card: Card, index: int) -> bool:
        '''Adds a card to the pile at a given index.

        Parameters:
            - self
            - card: Card object to be added to pile
            - index: int, where the card should be inserted

        Returns:
            - bool: True if successful addition, False otherwise
        '''
        if index > len(self.stack):
            return False
        else:
            self.stack.insert(index, card)
            return True
        
    def get_top(self) -> Card:
        '''Returns the top card of the pile.'''
        return self.stack[0]
    
    def draw(self) -> Card:
        '''Removes a card from the top of the pile. Returns that card.
        
        Parameters:
            - self

        Returns:
            - Card: top card, None if no cards in pile
        '''
        if len(self.stack) == 0:
            return None
        else:
            out = self.stack[0]
            self.stack.pop(0)
            return out
    
    def clear_all(self) -> None:
        '''Clears the stack.'''
        self.stack.clear()
        return

    def __str__(self) -> str:
        '''String representation of the pile.'''
        out = ''
        for i in range(len(self.stack)):
            out += str(i+1) + '.\t' + str(self.stack[i]) + '\n'
        return out

    def __len__(self) -> int:
        '''Returns the length of the stack'''
        return len(self.stack)
            
    
