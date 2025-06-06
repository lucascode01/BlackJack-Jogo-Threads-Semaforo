# game_logic.py

def print_welcome():
    print("=" * 40)
    print("🂡 Blackjack 31 - Sistema de Threads")
    print("=" * 40)

def ask_round():
    while True:
        answer = input("Deseja jogar outra rodada? (s/n): ").strip().lower()
        if answer in ("s", "n"):
            return answer == "s"
