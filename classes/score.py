class Score:

    global_score = 0.0

    def __init__(self, delta):
        self.delta = delta

    def active(self):
        Score.global_score = Score.global_score + self.delta

