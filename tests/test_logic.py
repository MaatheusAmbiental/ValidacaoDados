# tests/test_logic.py
def test_tolerance_logic():
    val_db = 10.54
    val_file = 10.61
    # Simula a lógica do SQL: ABS(ROUND(p - i, 1)) <= 0.1
    diff = abs(round(val_db, 1) - round(val_file, 1))
    assert diff <= 0.1  # Deve passar
