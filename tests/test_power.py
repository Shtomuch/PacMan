import pytest

from classes.global_vars import GlobalVars
from classes.power import Power


# Фікстура для скидання стану Power перед кожним тестом
@pytest.fixture(autouse=True)
def reset_power():
    Power.reset()
    GlobalVars.power_is_active = False
    yield
    Power.reset()
    GlobalVars.power_is_active = False


@pytest.mark.unit
def test_activate_sets_next_move_and_increments_count():
    """
    Перевіряє метод Power.activate:
    - Ініціалізує Power.next_move, якщо він ще не встановлений;
    - Збільшує лічильник Power.count на 1.
    """
    assert Power.next_move is None
    initial_count = Power.count
    Power.activate()
    assert Power.next_move is not None, "next_move має бути ініціалізовано"
    assert Power.count == initial_count + 1


@pytest.mark.unit
def test_update_activates_power_when_inactive():
    """
    Перевіряє метод Power.update:
    - Якщо power неактивний (GlobalVars.power_is_active == False) і Power.count > 0,
      то update активує power (встановлює power_is_active в True), обнуляє таймер і зменшує count.
    """
    # Якщо power не активний, а count > 0, то update має активувати power
    Power.count = 2
    GlobalVars.power_is_active = False
    Power.update(0.1)
    assert GlobalVars.power_is_active
    assert Power.count == 1
    assert Power._timer == 0


@pytest.mark.unit
@pytest.mark.parametrize("delta,initial_timer,expected_active", [
    (5, 0, True),  # timer не перевищує duration
    (11, 0, False)  # timer перевищує duration
])
def test_update_when_power_active(delta, initial_timer, expected_active):
    """
    Перевіряє метод Power.update, коли power активний.
    """
    GlobalVars.power_is_active = True
    Power._timer = initial_timer
    Power.duration = 10
    Power.update(delta)
    assert GlobalVars.power_is_active == expected_active


@pytest.mark.unit
def test_reset_clears_power_state():
    """
    Перевіряє метод Power.reset:
    - Обнуляє лічильник Power.count;
    - Обнуляє таймер Power._timer;
    - Встановлює GlobalVars.power_is_active в False.
    """
    Power.count = 5
    Power._timer = 5
    GlobalVars.power_is_active = True
    Power.reset()
    assert Power.count == 0
    assert Power._timer == 0
    assert GlobalVars.power_is_active == False
