

from game.dealer import Dealer
from game.player import Player
from game.game_logic import print_welcome, ask_round

def main():
    print_welcome()

    num_players = 3
    dealer = Dealer(num_players)
    players = [Player(i, dealer, dealer.turn_sem, dealer.done_sem) for i in range(num_players)]

    for p in players:
        p.start()

    try:
        while True:
            dealer.start_round()
            dealer.show_results()
            if not ask_round():
                break
    finally:
        dealer.end_game()
        for p in players:
            p.join()

    print("Jogo encerrado. Obrigado por jogar!")

if __name__ == "__main__":
    main()