from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'segredo'

MAX_SCORE = 21

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['players'] = [
            {'name': request.form.get('nome1', 'Jogador 1'), 'score': 0, 'log': '', 'standing': False},
            {'name': request.form.get('nome2', 'Jogador 2'), 'score': 0, 'log': '', 'standing': False},
            {'name': request.form.get('nome3', 'Jogador 3'), 'score': 0, 'log': '', 'standing': False}
        ]
        session['current_player'] = 0
        session['game_over'] = False
        session['logs'] = ["Starting a new round..."]
        return redirect(url_for('jogo'))
    return render_template('index.html')

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    players = session.get('players', [])
    current = session.get('current_player', 0)
    logs = session.get('logs', [])

    if session.get('game_over', False):
        scores = [p['score'] if p['score'] <= MAX_SCORE else 0 for p in players]
        max_score = max(scores)
        winner = None
        if max_score > 0:
            winner = players[scores.index(max_score)]['name']
        return render_template('index.html', resultados={p['name']: p['score'] for p in players}, vencedor=winner, logs="\n".join(logs))

    if request.method == 'POST':
        action = request.form['action']
        player = players[current]

        if action == 'hit':
            card = random.randint(1, 11)
            player['score'] += card
            log = f"{player['name']} comprou {card}, total: {player['score']}"
            player['log'] += log + "\n"
            logs.append(log)

            if player['score'] >= MAX_SCORE:
                player['standing'] = True

        elif action == 'stand':
            player['standing'] = True
            logs.append(f"{player['name']} decidiu parar com {player['score']} pontos.")

        session['players'] = players
        session['logs'] = logs

        # avançar para próximo jogador
        next_index = (current + 1) % len(players)
        while players[next_index]['standing']:
            next_index = (next_index + 1) % len(players)
            if next_index == current:
                session['game_over'] = True
                break

        session['current_player'] = next_index

        return redirect(url_for('jogo'))

    jogador_atual = players[current]
    return render_template('index.html', jogador=jogador_atual['name'], pontuacao=jogador_atual['score'], logs="\n".join(logs))

if __name__ == '__main__':
    app.run(debug=True)