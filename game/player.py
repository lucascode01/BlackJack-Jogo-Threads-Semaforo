import threading
import random
import time

class Player(threading.Thread):
    def __init__(self, player_id, dealer, turn_sem, done_sem):
        super().__init__()
        self.player_id = player_id
        self.name = f"Jogador {player_id + 1}"
        self.dealer = dealer
        self.turn_sem = turn_sem
        self.done_sem = done_sem
        self.score = 0
        self.max_score = 21

    def draw_card(self):
        return random.randint(1, 11)

    def run(self):
        while True:
            self.turn_sem[self.player_id].acquire()
            if self.dealer.game_over:
                break
            print(f"{self.name} está jogando...")
            self.score = 0
            while self.score < self.max_score:
                card = self.draw_card()
                self.score += card
                print(f"{self.name} comprou {card}, total: {self.score}")
                time.sleep(0.5)
                if self.score >= self.max_score:
                    break
            self.dealer.player_scores[self.player_id] = self.score
            self.done_sem[self.player_id].release()
