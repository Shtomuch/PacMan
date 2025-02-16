class NextMove:
    """
    Клас для управління чергою подій у грі.
    """
    list_of_events: list[list] = []
    queue: dict[str, int] = {
        'tile': 0,
        'point': 1,
        'power': 2,
        'pacman': 3,
        'ghost': 4,
        'interface': 5
    }

    def __init__(self, name: str, func: callable) -> None:
        """
        Ініціалізація події.
        :param name: Назва події.
        :param func: Функція, що виконується при активації події.
        """
        self.id: int = NextMove.queue[name]
        self.func: callable = func
        self.add_func()

    def add_func(self) -> None:
        """
        Додає функцію до відповідної категорії у списку подій.
        """
        while len(NextMove.list_of_events) <= self.id:
            NextMove.list_of_events.append([])
        NextMove.list_of_events[self.id].append(self.func)

    @staticmethod
    def activate(delta: float) -> None:
        """
        Виконує всі зареєстровані події у порядку пріоритету.
        :param delta: Значення, що передається у функції подій.
        """
        for list_of_events in NextMove.list_of_events:
            for func in list_of_events:
                func(delta)

    def remove_func(self) -> None:
        """
        Видаляє функцію з відповідної категорії подій.
        """
        if 0 <= self.id < len(NextMove.list_of_events):
            if self.func in NextMove.list_of_events[self.id]:
                NextMove.list_of_events[self.id].remove(self.func)
