import random

class Deck:
    def __init__(self):
        """
        Инициализирует колоду карт.
        """
        self.suits = ['♠', '♣', '♦', '♥']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [f"{value}{suit}" for value in self.values for suit in self.suits]
        self.shuffle()

    def shuffle(self):
        """
        Перетасовывает колоду карт.
        """
        random.shuffle(self.cards)

    def draw(self):
        """
        Извлекает одну карту из колоды.

        Returns:
            str: Карта в формате "рангмасть" (например, "A♠").
            None: Если колода пуста.
        """
        if not self.cards:
            return None
        return self.cards.pop()

    def reset(self):
        """
        Сбрасывает колоду, создавая новую и перетасовывая её.
        """
        self.cards = [f"{value}{suit}" for value in self.values for suit in self.suits]
        self.shuffle()

    def __len__(self):
        """
        Возвращает количество оставшихся карт в колоде.

        Returns:
            int: Количество карт в колоде.
        """
        return len(self.cards)

    def __repr__(self):
        """
        Возвращает строковое представление колоды.

        Returns:
            str: Описание колоды.
        """
        return f"Deck(cards={len(self.cards)})"