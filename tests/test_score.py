import pytest
from classes.global_vars import GlobalVars
from classes.score import Score

@pytest.fixture(scope="module")
def reset_global_vars():
    """Скидає глобальний рахунок перед кожним тестом."""
    GlobalVars.score = 0

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
def test_score_active_adds_points(delta, expected_score):
    """Перевіряємо, чи метод active додає очки до глобального рахунку."""
    s = Score(delta)
    s.active()
    assert GlobalVars.score == expected_score