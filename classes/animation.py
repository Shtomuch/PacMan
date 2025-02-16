class Animation:
    """
    Клас для управління анімацією на основі наборів анімацій.
    """

    def __init__(self, sets: list[AnimationSet], coordinates):
        """
        Ініціалізація об'єкта анімації.

        :param sets: Список доступних анімацій
        :param coordinates: Позиція, де відображається анімація
        """
        self.sets = sets
        self.position = coordinates
        self.animation_set = self.sets[0]
        self.direction = 0
        self.freeze = False

