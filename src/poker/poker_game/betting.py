from typing import List
from src.poker.agents.random_agent import RandomAgent
from src.poker.poker_game.game import PokerGame
from src.poker.poker_game.hand_evaluation import evaluate_hand  # Реализация функций для вычисления силы руки

def determine_winner(agents: List[RandomAgent], community_cards: List[str]) -> List[RandomAgent]:
    """
    Определяет победителя (или победителей в случае ничьей) по комбинациям.

    Args:
        agents (List[RandomAgent]): Список агентов.
        community_cards (List[str]): Общие карты.

    Returns:
        List[RandomAgent]: Список победителей.
    """
    best_score = None
    winners = []

    for agent in agents:
        if agent.active:
            # Используем функцию evaluate_hand для расчета силы руки
            print(agent.cards)
            print(community_cards)
            print(agent.cards + community_cards)
            hand_score = evaluate_hand(agent.cards + community_cards)
            print(f"{agent.name} комбинация: {hand_score['combination_name']} (оценка: {hand_score['score']})")

            # Сравниваем текущую комбинацию с лучшей
            if best_score is None or hand_score['score'] > best_score:
                best_score = hand_score['score']
                winners = [agent]
            elif hand_score['score'] == best_score:
                winners.append(agent)

    return winners

def distribute_pot(winners: List[RandomAgent], pot: int):
    """
    Распределяет банк между победителями.

    Args:
        winners (List[RandomAgent]): Список победителей.
        pot (int): Размер банка.
    """
    if not winners:
        raise ValueError("Нет победителей для распределения банка.")

    share = pot // len(winners)
    for winner in winners:
        winner.money += share
        print(f"{winner.name} получает {share} из банка!")

    # Обработка остатка
    remainder = pot % len(winners)
    if remainder > 0:
        winners[0].money += remainder
        print(f"{winners[0].name} получает дополнительно {remainder} из остатка банка.")

def betting_round(agents: List[RandomAgent], min_bet: int, current_bet: int, pot: int, community_cards: List[str], small_blind: int, big_blind: int, round_number: int):
    """
    Проводит один раунд ставок.

    Args:
        agents (List[RandomAgent]): Список агентов, участвующих в раунде.
        min_bet (int): Минимальная ставка для входа в раунд.
        current_bet (int): Текущая ставка, которую нужно "догнать".
        pot (int): Текущий банк.
        community_cards (List[str]): Общие карты.
        small_blind (int): Размер малого блайнда.
        big_blind (int): Размер большого блайнда.
        round_number (int): Номер раунда (0 — префлоп, 1 — флоп и т.д.).

    Returns:
        int: Обновлённый банк (pot).
        int: Обновлённая текущая ставка (current_bet).
    """
    small_blind_agent = agents[0]
    big_blind_agent = agents[1]

    # Обработка малого и большого блайндов (только в префлопе)
    if round_number == 0:
        # Малый блайнд
        if small_blind_agent.money >= small_blind:
            small_blind_agent.money -= small_blind
            small_blind_agent.current_bet = small_blind
            pot += small_blind
            print(f"{small_blind_agent.name} поставил малый блайнд: {small_blind}")
        else:
            pot += small_blind_agent.money
            small_blind_agent.current_bet = small_blind_agent.money
            small_blind_agent.money = 0
            print(f"{small_blind_agent.name} поставил всё (малый блайнд): {small_blind_agent.current_bet}")

        # Большой блайнд
        if big_blind_agent.money >= big_blind:
            big_blind_agent.money -= big_blind
            big_blind_agent.current_bet = big_blind
            pot += big_blind
            current_bet = big_blind
            print(f"{big_blind_agent.name} поставил большой блайнд: {big_blind}")
        else:
            pot += big_blind_agent.money
            big_blind_agent.current_bet = big_blind_agent.money
            big_blind_agent.money = 0
            current_bet = big_blind_agent.current_bet
            print(f"{big_blind_agent.name} поставил всё (большой блайнд): {big_blind_agent.current_bet}")

    # Игроки делают ходы начиная с игрока после большого блайнда
    pending_action = True
    flag = 0
    while pending_action:
        pending_action = False
        
        for agent in agents:
            if round_number == 0 and (agent == small_blind_agent or agent == big_blind_agent) and flag != 2:
                flag += 1
                continue
            if not agent.active:
                continue

            # Проверка, остался ли только один активный игрок
            if handle_one_player_left(agents, pot):
                return pot, current_bet

            amount_to_call = current_bet - agent.current_bet
            print(f"{agent.name}: нужно поставить {amount_to_call} для колла (текущая ставка: {current_bet}, текущая ставка агента: {agent.current_bet})")

            # Агент принимает решение
            decision, amount = agent.make_decision(
                community_cards=community_cards,
                current_bet=current_bet,
                pot=pot,
                min_bet=min_bet,
            )

            # Обработка решения агента
            if decision == "fold":
                agent.active = False
                print(f"{agent.name} решил fold (ставка: 0, остаток: {agent.money})")

            elif decision == "call":
                if amount_to_call > 0:
                    if agent.money >= amount_to_call:
                        agent.money -= amount_to_call
                        pot += amount_to_call
                        agent.current_bet += amount_to_call
                        
                        print(f"{agent.name} решил call (ставка: {agent.current_bet}, остаток: {agent.money})")
                    else:
                        pot += agent.money
                        agent.current_bet += agent.money
                        agent.money = 0
                        print(f"{agent.name} делает all-in (текущая ставка агента: {agent.current_bet}, остаток: 0)")
                else:
                    print(f"{agent.name} уже уравнял текущую ставку.")

            elif decision == "raise":
                if amount + agent.current_bet > current_bet:
                    raise_amount = amount # - agent.current_bet
                    if agent.money >= raise_amount + current_bet:
                        if agent.current_bet == 0:
                            agent.money -= current_bet
                            agent.current_bet = current_bet
                            pot += current_bet
                        agent.current_bet += raise_amount
                        agent.money -= raise_amount
                        pot += raise_amount
                        current_bet += raise_amount
                        print(f"{agent.name} решил raise на {raise_amount} (текущая ставка агента: {agent.current_bet}, остаток: {agent.money})")
                        pending_action = True
                    else:
                        print(f"{agent.name} не может сделать raise на {raise_amount}. Делает фолд.")
                        agent.active = False
                else:
                    print(f"{agent.name} не может сделать raise на меньшую сумму. Фолд.")
                    agent.active = False

            elif decision == "check":
                print(f"{agent.name} решил check (ставка: {agent.current_bet}, остаток: {agent.money})")

        # Проверка, уравняли ли все активные игроки текущую ставку
        for agent in agents:
            if agent.active and agent.current_bet < current_bet:
                pending_action = True
                break

    return pot, current_bet

def handle_one_player_left(agents: List[RandomAgent], pot: int) -> bool:
    """
    Завершает раздачу, если остался только один активный игрок.

    Args:
        agents (List[RandomAgent]): Список всех агентов.
        pot (int): Текущий банк.

    Returns:
        bool: True, если раздача завершена, иначе False.
    """
    active_agents = [agent for agent in agents if agent.active]
    if len(active_agents) == 1:
        winner = active_agents[0]
        winner.money += pot
        print(f"{winner.name} выиграл банк: {pot}!")
        return True
    return False

def manage_betting_rounds(agents: List[RandomAgent], min_bet: int, game: PokerGame, small_blind: int, big_blind: int):
    """
    Управляет раундами ставок в игре, включая повторное уравнивание ставок.

    Args:
        agents (List[RandomAgent]): Список агентов.
        min_bet (int): Минимальная ставка для входа в игру.
        game (PokerGame): Игра.
        small_blind (int): Размер малого блайнда.
        big_blind (int): Размер большого блайнда.
    """
    current_bet = min_bet
    pot = 0

    for round_number in range(4):  # Префлоп, флоп, терн, ривер
        print(f"\nРаунд ставок {round_number + 1}:")
        if round_number == 0:
            print("Префлоп")
        elif round_number == 1:
            game.deal_community_cards(3)  # Флоп
        else:
            game.deal_community_cards(1)  # Терн и ривер

        print(f"Общие карты: {game.community_cards}")
        pot, current_bet = betting_round(agents, min_bet, current_bet, pot, game.community_cards, small_blind, big_blind, round_number)

        # Проверка, остался ли только один игрок
        if handle_one_player_left(agents, pot):
            return

    # Шоудаун, если осталось несколько игроков
    active_agents = [agent for agent in agents if agent.active]
    if len(active_agents) > 1:
        print("Все дошли до шоудауна. Определяем победителя...")
        winners = determine_winner(active_agents, game.community_cards)
        distribute_pot(winners, pot)
    else:
        print("Игроков недостаточно для шоудауна. Игра завершена.")