from typing import List
from src.poker.agents.random_agent import RandomAgent
from src.poker.poker_game.game import PokerGame

def betting_round(agents: List[RandomAgent], min_bet: int, current_bet: int, pot: int, community_cards: List[str]):
    """
    Проводит один раунд ставок.

    Args:
        agents (List[RandomAgent]): Список агентов, участвующих в раунде.
        min_bet (int): Минимальная ставка для входа в раунд.
        current_bet (int): Текущая ставка, которую нужно "догнать".
        pot (int): Текущий банк.
        community_cards (List[str]): Общие карты.

    Returns:
        int: Обновлённый банк (pot).
        int: Обновлённая текущая ставка (current_bet).
    """
    pending_action = True  # Пока кто-то делает raise, раунд продолжается

    while pending_action:
        pending_action = False  # Сброс флага; будет установлен, если кто-то сделает raise

        for agent in agents:
            if not agent.active:  # Пропускаем агентов, сделавших fold
                continue

            # Сколько нужно уравнять для текущего игрока
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

            elif decision == "call":
                if amount_to_call > 0:
                    # Уравниваем ставку
                    if agent.money >= amount_to_call:
                        agent.money -= amount_to_call
                        agent.current_bet += amount_to_call
                        pot += amount_to_call
                        print(f"{agent.name} решил call (ставка: {amount_to_call}, остаток: {agent.money})")
                    else:
                        # Если не хватает денег, агент идёт all-in
                        pot += agent.money
                        agent.current_bet += agent.money
                        agent.money = 0
                        print(f"{agent.name} делает all-in (ставка: {agent.current_bet}, остаток: 0)")
                else:
                    print(f"{agent.name} уже уравнял текущую ставку.")

            elif decision == "raise":
                if amount > current_bet:
                    raise_amount = amount - current_bet
                    if agent.money >= raise_amount:
                        # Устанавливаем новую текущую ставку
                        agent.money -= raise_amount
                        agent.current_bet += raise_amount
                        pot += raise_amount
                        current_bet = amount
                        print(f"{agent.name} решил raise (ставка: {amount}, остаток: {agent.money})")
                        pending_action = True  # Устанавливаем флаг для продолжения раунда
                    else:
                        print(f"{agent.name} не может сделать raise на {amount}. Выбывает из игры.")
                        agent.active = False
                else:
                    print(f"{agent.name} не может сделать raise на меньшую сумму. Пропускает ход.")

        # Проверяем, уравняли ли все активные игроки текущую ставку
        for agent in agents:
            if agent.active and agent.current_bet < current_bet:
                pending_action = True
                break

    # В конце раунда сохраняем ставки игроков для следующего этапа
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


def manage_betting_rounds(agents: List[RandomAgent], min_bet: int, game: PokerGame):
    """
    Управляет раундами ставок в игре, включая повторное уравнивание ставок.

    Args:
        agents (List[Agent]): Список агентов.
        min_bet (int): Минимальная ставка для входа в игру.
        community_cards (List[str]): Общие карты на столе.
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
        pot, current_bet = betting_round(agents, min_bet, current_bet, pot, game.community_cards)

        # Проверяем, остался ли только один игрок
        if handle_one_player_left(agents, pot):

            return

        # Печатаем общие карты и текущий банк
        

    print("Ставки завершены. Продолжаем игру!")
