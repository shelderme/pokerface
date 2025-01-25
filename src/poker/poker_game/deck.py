import random

class Deck:
    def __init__(self):
        self.suits = ['♠', '♣', '♦', '♥']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [f"{value}{suit}" for value in self.values for suit in self.suits]
        random.shuffle(self.cards)
    
    def draw(self):
        """Извлекает одну карту из колоды."""
        return self.cards.pop() if self.cards else None
    
    def reshuffle(self):
        """Перетасовать колоду."""
        self.cards = [f"{value}{suit}" for value in self.values for suit in self.suits]
        random.shuffle(self.cards)
