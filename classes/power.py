
from classes.global_vars import GlobalVars
from classes.next_move import NextMove


class Power:

    count = 0

    duration = 10
    _timer = 0
    next_move = None

    @staticmethod
    def update(delta):
        if not GlobalVars.power_is_active:
            if Power.count > 0:
                Power._timer = 0
                Power.count -= 1
                GlobalVars.power_is_active = True
            return

        Power._timer += delta
        if Power._timer > Power.duration:
            GlobalVars.power_is_active = False

    @staticmethod
    def activate():
        if Power.next_move is None:
            Power.next_move = NextMove('power', Power.update)
        Power.count += 1

    @staticmethod
    def reset():
        Power.count = 0
        Power._timer = 0
        GlobalVars.power_is_active = False
