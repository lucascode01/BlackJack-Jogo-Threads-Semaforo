from flask import Flask, render_template, request
import threading
from game.player import Player
from game.dealer import Dealer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome1 = request.form.get('nome1') or 'Jogador 1'
        nome2 = request.form.get('nome2') or 'Jogador 2'
        nome3 = request.form.get('nome3') or 'Jogador 3'
        nomes = [nome1, nome2, nome3]

        num_players = 3
        dealer = Dealer(num_players)
        turn_sems = [threading.Semaphore(0) for _ in range(num_players)]
        done_sems = [threading.Semaphore(0) for _ in range(num_players)]

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

        resultados = {j.name: j.score for j in jogadores}
        vencedor_id = dealer.get_winner()
        vencedor = jogadores[vencedor_id].name if vencedor_id is not None else None
        logs = "\n".join(j.logs for j in jogadores)

        return render_template('index.html', resultados=resultados, vencedor=vencedor, logs=logs)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)