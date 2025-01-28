from coordinates import Coordinate

class MoveUnit:

    def __init__(self, im, x, y):
        self.im = im
        self.coords = Coordinate(x, y)