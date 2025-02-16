# from classes import ghost


class NextMove:
    list_of_events = []
    queue = {'tile': 0, 'point': 1, 'power': 2, 'pacman': 3, 'ghost': 4, 'interface': 5}


    def __init__(self, name, func):
        self.id = NextMove.queue[name]
        self.func = func
        self.add_func()

    def add_func(self):
        # Расширяем список до нужной длины
        while len(NextMove.list_of_events) <= self.id:
            NextMove.list_of_events.append([])
        NextMove.list_of_events[self.id].append(self.func)

    @staticmethod
    def activate(delta):
        """
        По идее, список событий может быть многомерным, где [0] – это самые
        приоритетные, [1] – второстепенные и т.д.
        короч просто в слоте 0.
        """
        for list_of_events in NextMove.list_of_events:
            for func in list_of_events:
                func(delta)

    def remove_func(self):
        if 0 <= self.id < len(NextMove.list_of_events):
            if self.func in NextMove.list_of_events[self.id]:
                NextMove.list_of_events[self.id].remove(self.func)
