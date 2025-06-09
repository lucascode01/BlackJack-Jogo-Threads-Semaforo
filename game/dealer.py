import threading

class Dealer:
    def __init__(self, num_players):
        self.num_players = num_players
        self.player_scores = [0] * num_players
        self.turn_sem = None
        self.done_sem = None
        self.game_over = False

    def start_round(self):
        print("\nStarting a new round...")
        for i in range(self.num_players):
            self.turn_sem[i].release()

        for i in range(self.num_players):
            self.done_sem[i].acquire()

    def show_results(self):
        print("\nRound finished. Results:")
        for i, score in enumerate(self.player_scores):
            print(f"Player {i} scored {score}")
        winner = self.get_winner()
        if winner is not None:
            print(f"\nPlayer {winner} wins!")
        else:
            print("\nAll players busted. No winner.")

    def get_winner(self):
        max_score = -1
        winner = None
        for i, score in enumerate(self.player_scores):
            if score <= 21 and score > max_score:
                max_score = score
                winner = i
        return winner

    def end_game(self):
        self.game_over = True
        if self.turn_sem:
            for sem in self.turn_sem:
                sem.release()
