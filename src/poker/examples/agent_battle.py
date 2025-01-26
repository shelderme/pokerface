
from src.poker.poker_game.deck import Deck
from src.poker.poker_game.game import PokerGame
from src.poker.agents.random_agent import RandomAgent
from src.poker.poker_game.betting import manage_betting_rounds
def play_game():
    # Создаем агентов
    num_agents = 3
    agents = [RandomAgent(f"Agent {i+1}") for i in range(num_agents)]

    # Создаем игру
    game = PokerGame(num_players=num_agents)
    game.players = agents  # Подставляем агентов вместо стандартных игроков

    # Начинаем игру
    print("Начало игры: Texas Hold'em Poker")
    game.deal_cards()

    # Вывод карт агентов
    for agent in agents:
        print(f"{agent.name} получил карты: {agent.cards}")

    # Раунд ставок
    min_bet = 10

    manage_betting_rounds(agents=agents, min_bet=min_bet, small_blind=10, big_blind=20, game=game)
   
    # Определяем победителя
    winner = game.determine_winner()
    print(f"\nПобедитель: {winner.name}")

    # Обновляем состояние игры
    game.reset_game()


if __name__ == "__main__":
    play_game()
