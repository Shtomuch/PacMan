import pytest
from classes.global_vars import GlobalVars
from classes.score import Score

@pytest.fixture
def reset_global_vars():
    """Скидає GlobalVars.score тільки перед першим тестом у параметризованому наборі."""
    if not hasattr(reset_global_vars, "score_reset_done"):
        GlobalVars.score = 0
        reset_global_vars.score_reset_done = True

def test_score_initialization():
    """Перевіряємо правильність ініціалізації об'єкта Score."""
    s = Score(10)
    assert s.delta == 10

@pytest.mark.parametrize("delta, expected_score", [
    (5, 5),
    (7, 12),  # 5 + 7
    (-3, 9),  # 12 - 3
    (10, 19), # 9 + 10
])
def test_score_active_adds_points(delta, expected_score, reset_global_vars):
    """Перевіряємо, чи метод active додає очки до глобального рахунку."""
    s = Score(delta)
    s.active()
    assert GlobalVars.score == expected_score