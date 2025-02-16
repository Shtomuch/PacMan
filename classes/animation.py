
class Animation:
    def __init__(self, sets, coordinates):
        """
        sets – список об'єктів AnimationSet, які містять кадри анімації.
        coordinates – позиція, де буде відображатися анімація.
        """
        self.sets = sets
        self.position = coordinates
        self.animation_set = self.sets[0]
        self.direction = 0
        self.freeze = False

    @property
    def current_animation(self):
        return self.animation_set.name

    @current_animation.setter
    def current_animation(self, value):
        if value == self.current_animation:
            return
        for anim_set in self.sets:
            if anim_set.name == value:
                self.animation_set = anim_set
                return
        self.animation_set = self.sets[0]

    def update(self, delta):
        """Оновлюємо анімацію та відображаємо її, якщо потрібно."""
        self.animation_set.direction = self.direction
        if self.freeze:
            # Якщо анімація заморожена, просто відображаємо поточний кадр
            self.animation_set.draw(self.position)
        else:
            self.animation_set.update(delta, self.position)