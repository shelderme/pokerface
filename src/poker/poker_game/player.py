class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []  # Две закрытые карты
        self.money = 1000  # Начальная сумма денег
        self.bet = 0  # Текущая ставка
    
    def receive_cards(self, cards):
        """Получить карты от дилера."""
        self.cards = cards

    def make_bet(self, amount):
        """Сделать ставку."""
        self.bet = amount
        self.money -= amount

    def fold(self):
        """Сдать карты."""
        self.cards = []

    def reset(self):
        """Сбросить ставки и карты."""
        self.bet = 0
        self.cards = []

    def is_broke(self):
        """Проверка, что у игрока нет денег."""
        return self.money <= 0
