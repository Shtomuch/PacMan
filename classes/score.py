class Score:
    """
    Клас для керування глобальним рахунком.
    """
    global_score: float = 0.0

    def __init__(self, delta: float) -> None:
        """
        Ініціалізація екземпляра класу.
        :param delta: Значення, на яке змінюється глобальний рахунок.
        """
        self.delta: float = delta

    def active(self) -> None:
        """
        Додає значення delta до глобального рахунку.
        """
        Score.global_score += self.delta
