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

    @property
    def current_animation(self) -> str:
        """
        Повертає назву поточної анімації.
        """
        return self.animation_set.name

    @current_animation.setter
    def current_animation(self, value: str) -> None:
        """
        Змінює поточну анімацію, якщо знайдено відповідну назву.

        :param value: Назва нової анімації
        """
        if value == self.current_animation:
            return

        for anim_set in self.sets:
            if anim_set.name == value:
                self.animation_set = anim_set
                return

        self.animation_set = self.sets[0]

    def update(self, delta: float) -> None:
        """
        Оновлює анімацію та малює її, якщо необхідно.

        :param delta: Час, що минув з останнього оновлення
        """
        self.animation_set.direction = self.direction
        if self.freeze:
            self.animation_set.draw(self.position)
        else:
            self.animation_set.update(delta, self.position)