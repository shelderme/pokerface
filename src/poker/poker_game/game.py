from .deck import Deck
from .player import Player
import random

class PokerGame:
    def __init__(self, num_players):
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.deck = Deck()  # Колода карт
        self.pot = 0  # Пот
        self.community_cards = []  # Общие карты
        self.round = 0  # Текущий раунд (потенциально префлоп, флоп, терн, ривер)
    
    def deal_cards(self):
        """Раздать карты игрокам."""
        for player in self.players:
            player.receive_cards([self.deck.draw(), self.deck.draw()])

    def deal_community_cards(self, count):
        """Раздать общие карты (флоп, терн, ривер)."""
        self.community_cards.extend([self.deck.draw() for _ in range(count)])

    def betting_round(self):
        """Раунд ставок. Здесь можно использовать агентов для принятия решений."""
        for player in self.players:
            if player.is_broke():
                continue
            bet = random.randint(10, 100)  # Простая ставка для примера
            player.make_bet(bet)
            self.pot += bet

    def determine_winner(self):
        """Определение победителя."""
        return random.choice(self.players)  # Для начала просто выбираем случайного игрока

    def reset_game(self):
        """Сброс игры после раунда."""
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.reset()
        self.deck.shuffle()
