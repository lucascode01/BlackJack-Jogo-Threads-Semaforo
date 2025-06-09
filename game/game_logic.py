# game_logic.py

def print_welcome():
    print("=" * 40)
    print("🂡 Blackjack 21 - Sistema de Threads")
    print("=" * 40)

def ask_round():
    while True:
        answer = input("Deseja jogar outra rodada? (s/n): ").strip().lower()
        if answer in ("s", "n"):
            return answer == "s"


# Função para jogar uma rodada de Blackjack
def jogar_rodada(jogador, dealer):
    jogador.mao = []
    dealer.mao = []

    jogador.receber_carta()
    jogador.receber_carta()
    dealer.receber_carta()
    dealer.receber_carta()

    while jogador.pontuacao() < 17:
        jogador.receber_carta()

    while dealer.pontuacao() < 17:
        dealer.receber_carta()

    print(f"{jogador.nome}: {jogador.pontuacao()} pontos")
    print(f"Dealer: {dealer.pontuacao()} pontos")

    if jogador.pontuacao() > 21:
        print(f"{jogador.nome} estourou! Dealer vence.")
    elif dealer.pontuacao() > 21 or jogador.pontuacao() > dealer.pontuacao():
        print(f"{jogador.nome} venceu!")
    elif jogador.pontuacao() < dealer.pontuacao():
        print("Dealer venceu.")
    else:
        print("Empate.")
