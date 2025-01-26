from typing import List
from src.poker.agents.random_agent import RandomAgent
from src.poker.poker_game.game import PokerGame

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

    Returns:
        int: Обновлённый банк (pot).
        int: Обновлённая текущая ставка (current_bet).
    """
    small_blind_agent = agents[0]
    big_blind_agent = agents[1]
    if round_number == 0:
    # Устанавливаем ставки для малого и большого блайнда
    # Малый блайнд автоматически ставит small_blind
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

        # Большой блайнд автоматически ставит big_blind
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
    while pending_action:
        pending_action = False
        for agent in agents[2:] + [small_blind_agent, big_blind_agent]:
            if not agent.active:
                continue
            if handle_one_player_left(agents=agents, pot=pot):
                return pot, current_bet
            amount_to_call = current_bet - agent.current_bet

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
                if handle_one_player_left(agents=agents, pot=pot):
                    return pot, current_bet

            elif decision == "call":
                if amount_to_call > 0:
                    if agent.money >= amount_to_call:
                        agent.money -= amount_to_call
                        agent.current_bet += amount_to_call
                        pot += amount_to_call
                        print(f"{agent.name} решил call (ставка: {agent.current_bet}, остаток: {agent.money})")
                    else:
                        pot += agent.money
                        agent.current_bet += agent.money
                        agent.money = 0
                        print(f"{agent.name} делает all-in (ставка: {agent.current_bet}, остаток: 0)")
                else:
                    print(f"{agent.name} уже уравнял текущую ставку.")

            elif decision == "raise":
                if amount > current_bet:
                    raise_amount = amount
                    if agent.money >= raise_amount:
                        agent.money -= raise_amount
                        agent.current_bet += raise_amount
                        pot += raise_amount
                        current_bet += amount
                        print(f"{agent.name} решил raise (ставка: {agent.current_bet}, остаток: {agent.money})")
                        pending_action = True
                    else:
                        print(f"{agent.name} не может сделать raise на {amount}. Выбывает из игры.")
                        agent.active = False
                else:
                    print(f"{agent.name} не может сделать raise на меньшую сумму. Пропускает ход.")
                    agent.active = False

            elif decision == "check":
                print(f"{agent.name} решил check (ставка: {agent.current_bet}, остаток: {agent.money})")

        if handle_one_player_left(agents=agents, pot=pot):
            return pot, current_bet

        # Проверяем, уравняли ли все активные игроки текущую ставку
        for agent in agents:
            if agent.active and agent.current_bet < current_bet:
                pending_action = True
                break

    return pot, current_bet


def check_active_players(agents: List[RandomAgent]) -> List[RandomAgent]:
    """
    Проверяет активных игроков в текущей раздаче.

    Args:
        agents (List[Agent]): Список всех агентов.

    Returns:
        List[Agent]: Список активных агентов.
    """
    return [agent for agent in agents if agent.active]


def handle_one_player_left(agents: List[RandomAgent], pot: int) -> bool:
    """
    Завершает раздачу, если остался только один активный игрок.

    Args:
        agents (List[Agent]): Список всех агентов.
        pot (int): Текущий банк.

    Returns:
        bool: True, если раздача завершена, иначе False.
    """
    active_agents = check_active_players(agents)
    if len(active_agents) == 1:
        winner = active_agents[0]
        winner.money += pot
        print(f"{winner.name} выиграл банк: {pot}!")
        return True  # Раздача завершена
    return False  # Продолжаем игру


def manage_betting_rounds(agents: List[RandomAgent], min_bet: int, game: PokerGame, small_blind: int, big_blind: int):
    """
    Управляет раундами ставок в игре, включая повторное уравнивание ставок.

    Args:
        agents (List[Agent]): Список агентов.
        min_bet (int): Минимальная ставка для входа в игру.
        small_blind (int): Размер малого блайнда.
        big_blind (int): Размер большого блайнда.
        game (PokerGame): Игра.
    """
    current_bet = min_bet
    pot = 0

    for round_number in range(4):  # Три раунда ставок
        print(f"Текущий пот: {pot}\nТекущая ставка: {current_bet}\n")
        print(f"\nРаунд ставок {round_number + 1}:")
        if round_number == 0:
            print("Префлоп")
        elif round_number == 1:
            game.deal_community_cards(3)
        else:
            game.deal_community_cards(1)
        print(f"Общие карты: {game.community_cards}")
        print(f"Текущий пот: {pot}\n")
        pot, current_bet = betting_round(agents, min_bet, current_bet, pot, game.community_cards, small_blind, big_blind, round_number)

        # Проверяем, остался ли только один игрок
        if handle_one_player_left(agents, pot):
            return

    print("Ставки завершены. Продолжаем игру!")