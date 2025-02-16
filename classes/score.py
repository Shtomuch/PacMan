from classes.global_vars import GlobalVars
class Score:

    def __init__(self, delta):
        self.delta = delta

    def active(self):
        """Добавляем очки к глобальному счёту."""
        GlobalVars.score += self.delta
