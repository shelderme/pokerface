import random

class RandomAgent:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.money = 1000  # Начальный баланс
        self.current_bet = 0
        self.active = True

    def receive_cards(self, cards):
        """Получить карты от дилера."""
        self.cards = cards

    def make_decision(self, community_cards, current_bet, pot, min_bet):
        """
        Принимает решение на основе текущей ситуации.
        Решение: случайный выбор между `fold`, `call`, `raise`.
        """
        if self.money <= 0:
            decision = "fold"
            return "fold", 0
        decision = []
        if current_bet == self.current_bet:  # Возможен чек
            actions = ["check", "raise"]
            decision = random.choice(actions)
        elif self.money <= min_bet:
            actions = ["fold", "call"]
            decision = random.choice(actions)
        else:
            actions = ["fold", "call", "raise"]
            decision = random.choice(actions)

        if decision == "fold":
            self.active = False
            return "fold", 0
        elif decision == "check":
            return "check", 0
        elif decision == "call":
            call_amount = current_bet - self.current_bet
            if call_amount > self.money:
                call_amount = self.money
            return "call", call_amount
        elif decision == "raise":
            raise_amount = random.randint(current_bet, current_bet * 3)
            return "raise", raise_amount

    def reset(self):
        """Сброс состояния агента перед следующим раундом."""
        self.cards = []
        self.current_bet = 0
