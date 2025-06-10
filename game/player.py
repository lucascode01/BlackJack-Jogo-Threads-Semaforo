import threading
import random
import time

class Player(threading.Thread):
    def __init__(self, player_id, dealer, turn_sem, done_sem, nome):
        super().__init__()
        self.player_id = player_id
        self.name = nome
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
            self.score = 0
            self.logs = f"{self.name} começou a jogar...\n"
            while self.score < self.max_score:
                if self.score >= 17:
                    break
                card = self.draw_card()
                self.score += card
                self.logs += f"{self.name} comprou {card}, total: {self.score}\n"
                time.sleep(0.5)
                if self.score >= self.max_score:
                    break
            self.dealer.player_scores[self.player_id] = self.score
            self.done_sem[self.player_id].release()
