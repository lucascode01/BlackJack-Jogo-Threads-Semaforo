import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import threading
from game.player import Player
from game.dealer import Dealer
from game.game_logic import pedir_nomes_jogadores

def main():
    dealer = Dealer(num_players=3)
    turn_sems = [threading.Semaphore(0) for _ in range(3)]
    done_sems = [threading.Semaphore(0) for _ in range(3)]

    nomes = pedir_nomes_jogadores(3)

    jogadores = [
        Player(0, dealer, turn_sems, done_sems, nomes[0]),
        Player(1, dealer, turn_sems, done_sems, nomes[1]),
        Player(2, dealer, turn_sems, done_sems, nomes[2])
    ]

    for jogador in jogadores:
        jogador.start()

    dealer.turn_sem = turn_sems
    dealer.done_sem = done_sems
    dealer.start_round()
    dealer.show_results()
    dealer.end_game()

    for jogador in jogadores:
        jogador.join()

    print("\nTodas as rodadas terminaram!")

if __name__ == "__main__":
    main()