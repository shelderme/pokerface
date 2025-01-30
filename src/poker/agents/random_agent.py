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
            weights = [0.7, 0.3]
            actions = ["check", "raise"]

            decision = random.choices(actions, weights=weights, k=1)[0]
        elif self.money <= min_bet:
            weights = [0.2, 0.8]
            actions = ["fold", "call"]
            decision = random.choices(actions, weights=weights, k=1)[0]
        else:
            weights = [0.2, 0.5, 0.3]
            actions = ["fold", "call", "raise"]
            decision = random.choices(actions, weights=weights, k=1)[0]

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
            raise_amount = random.randint(current_bet, current_bet + min_bet * 2)
            return "raise", raise_amount

    def reset(self):
        """Сброс состояния агента перед следующим раундом."""
        self.cards = []
        self.current_bet = 0
