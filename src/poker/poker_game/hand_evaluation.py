from collections import Counter
from typing import List, Dict

def evaluate_hand(cards: List[str]) -> Dict:
    """
    Определяет силу комбинации покерной руки.

    Args:
        cards (List[str]): Список карт (например, ['2H', '3D', '5S', '9C', 'KD']).

    Returns:
        Dict: Словарь с комбинацией и её оценкой.
    """
    ranks = '23456789TJQKA'
    suits = '♠♣♦♥'

    # Функция для получения рангов и мастей
    def get_rank(card):
        return card[0]

    def get_suit(card):
        return card[1]

    # Ранжируем карты
    rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}
    card_ranks = sorted([rank_values[get_rank(card)] for card in cards], reverse=True)
    card_suits = [get_suit(card) for card in cards]

    # Проверка на пары, тройки, каре и т.д.
    rank_counts = Counter(card_ranks)
    suit_counts = Counter(card_suits)

    is_flush = any(count >= 5 for count in suit_counts.values())
    is_straight = check_straight(card_ranks)
    is_straight_flush = is_flush and is_straight

    # Роял-флеш
    if is_straight_flush and max(card_ranks) == rank_values['A']:
        return {'combination_name': 'Royal Flush', 'score': 10000}

    # Стрит-флеш
    if is_straight_flush:
        return {'combination_name': 'Straight Flush', 'score': 9000 + max(card_ranks)}

    # Каре
    if 4 in rank_counts.values():
        quads_rank = [rank for rank, count in rank_counts.items() if count == 4][0]
        kicker = max([rank for rank in card_ranks if rank != quads_rank])
        return {'combination_name': 'Four of a Kind', 'score': 8000 + quads_rank * 10 + kicker}

    # Фулл-хаус
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        triplet = [rank for rank, count in rank_counts.items() if count == 3][0]
        pair = [rank for rank, count in rank_counts.items() if count == 2][0]
        return {'combination_name': 'Full House', 'score': 7000 + triplet * 10 + pair}

    # Флеш
    if is_flush:
        flush_cards = [rank for rank, suit in zip(card_ranks, card_suits) if suit_counts[suit] >= 5]
        return {'combination_name': 'Flush', 'score': 6000 + sum(flush_cards[:5])}

    # Стрит
    if is_straight:
        return {'combination_name': 'Straight', 'score': 5000 + max(card_ranks)}

    # Тройка
    if 3 in rank_counts.values():
        triplet = [rank for rank, count in rank_counts.items() if count == 3][0]
        kickers = sorted([rank for rank in card_ranks if rank != triplet], reverse=True)[:2]
        return {'combination_name': 'Three of a Kind', 'score': 4000 + triplet * 10 + sum(kickers)}

    # Две пары
    if list(rank_counts.values()).count(2) >= 2:
        pairs = sorted([rank for rank, count in rank_counts.items() if count == 2], reverse=True)[:2]
        kicker = max([rank for rank in card_ranks if rank not in pairs])
        return {'combination_name': 'Two Pair', 'score': 3000 + pairs[0] * 10 + pairs[1] + kicker}

    # Пара
    if 2 in rank_counts.values():
        pair = [rank for rank, count in rank_counts.items() if count == 2][0]
        kickers = sorted([rank for rank in card_ranks if rank != pair], reverse=True)[:3]
        return {'combination_name': 'One Pair', 'score': 2000 + pair * 10 + sum(kickers)}

    # Старшая карта
    return {'combination_name': 'High Card', 'score': 1000 + sum(card_ranks[:5])}


def check_straight(ranks: List[int]) -> bool:
    """
    Проверяет, есть ли стрит.

    Args:
        ranks (List[int]): Список рангов карт.

    Returns:
        bool: True, если стрит найден.
    """
    unique_ranks = sorted(set(ranks), reverse=True)
    for i in range(len(unique_ranks) - 4):
        if unique_ranks[i] - unique_ranks[i + 4] == 4:
            return True
    # Проверка на стрит с тузом в качестве единицы
    if set([14, 5, 4, 3, 2]).issubset(unique_ranks):
        return True
    return False
