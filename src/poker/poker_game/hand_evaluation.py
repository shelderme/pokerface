from itertools import combinations
from collections import Counter
from typing import List, Dict


def evaluate_hand(cards: List[str]) -> Dict:
    """
    Оценивает лучшую комбинацию покерной руки из пяти карт.

    Args:
        cards (List[str]): Список всех карт (7 карт: 2 на руках + 5 общих).

    Returns:
        Dict: Словарь с информацией о лучшей комбинации и её оценкой.
    """
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}

    def get_rank(card):
        return card[:-1]

    def get_suit(card):
        return card[1]

    def check_straight(ranks: List[int]) -> bool:
        """
        Проверяет, есть ли стрит (последовательность из 5 карт по рангам).
        Учитывает случай "колеса" (A-2-3-4-5).
        """
        unique_ranks = sorted(set(ranks), reverse=True)
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                return True
        if set([14, 5, 4, 3, 2]).issubset(unique_ranks):  # Для случая "колеса" (A-5)
            return True
        return False

    def get_hand_score(combo: List[str]) -> Dict:
        """
        Оценивает комбинацию из 5 карт и возвращает её название и оценку.
        """
        card_ranks = sorted([rank_values[get_rank(card)] for card in combo], reverse=True)
        card_suits = [get_suit(card) for card in combo]
        rank_counts = Counter(card_ranks)
        suit_counts = Counter(card_suits)

        is_flush = any(count >= 5 for count in suit_counts.values())
        is_straight = check_straight(card_ranks)
        is_straight_flush = is_flush and is_straight

        if is_straight_flush:
            if max(card_ranks) == rank_values['A']:
                return {'combination_name': 'Royal Flush', 'score': 10000}
            return {'combination_name': 'Straight Flush', 'score': 9000 + max(card_ranks)}

        if 4 in rank_counts.values():
            quads_rank = [rank for rank, count in rank_counts.items() if count == 4][0]
            kicker = max([rank for rank in card_ranks if rank != quads_rank])
            return {'combination_name': 'Four of a Kind', 'score': 8000 + quads_rank * 10 + kicker}

        if 3 in rank_counts.values() and 2 in rank_counts.values():
            triplet = [rank for rank, count in rank_counts.items() if count == 3][0]
            pair = [rank for rank, count in rank_counts.items() if count == 2][0]
            return {'combination_name': 'Full House', 'score': 7000 + triplet * 10 + pair}

        if is_flush:
            flush_cards = sorted([rank for rank, suit in zip(card_ranks, card_suits) if suit_counts[suit] >= 5], reverse=True)
            return {'combination_name': 'Flush', 'score': 6000 + sum(flush_cards[:5])}

        if is_straight:
            return {'combination_name': 'Straight', 'score': 5000 + max(card_ranks)}

        if 3 in rank_counts.values():
            triplet = [rank for rank, count in rank_counts.items() if count == 3][0]
            kickers = sorted([rank for rank in card_ranks if rank != triplet], reverse=True)[:2]
            return {'combination_name': 'Three of a Kind', 'score': 4000 + triplet * 10 + sum(kickers)}

        if list(rank_counts.values()).count(2) >= 2:
            pairs = sorted([rank for rank, count in rank_counts.items() if count == 2], reverse=True)[:2]
            kicker = max([rank for rank in card_ranks if rank not in pairs])
            return {'combination_name': 'Two Pair', 'score': 3000 + pairs[0] * 10 + pairs[1] + kicker}

        if 2 in rank_counts.values():
            pair = [rank for rank, count in rank_counts.items() if count == 2][0]
            kickers = sorted([rank for rank in card_ranks if rank != pair], reverse=True)[:3]
            return {'combination_name': 'One Pair', 'score': 2000 + pair * 10 + sum(kickers)}

        return {'combination_name': 'High Card', 'score': 1000 + sum(card_ranks[:5])}

    # Проверка на корректное количество карт
    if len(cards) != 7:
        raise ValueError("Должно быть ровно 7 карт для оценки комбинации.")

    best_hand = {'combination_name': '', 'score': 0}
    for combo in combinations(cards, 5):  # Перебираем все сочетания из 7 карт по 5
        hand_score = get_hand_score(list(combo))
        if hand_score['score'] > best_hand['score']:
            best_hand = hand_score

    return best_hand
#  #['♠', '♣', '♦', '♥']
# cards = ['4♣', '6♠', 'Q♠', '10♥', '8♠', '6♠', '3♣']  # Пример флеша
# result = evaluate_hand(cards)
# print(result)