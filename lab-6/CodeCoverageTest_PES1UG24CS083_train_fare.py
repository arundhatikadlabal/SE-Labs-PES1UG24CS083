"""Test cases for code (line) coverage of train_fare.py.

Every line of train_fare.py is executed at least once by these tests.
"""
import pytest
from train_fare import base_fare, concession, tatkal_charge


# ---------- base_fare ----------

def test_sleeper_fare():
    assert base_fare("SL", 500) == 500


def test_ac_three_tier_fare():
    assert base_fare("3A", 100) == 200


def test_first_ac_fare():
    assert base_fare("1A", 100) == 500


def test_minimum_fare_applied():
    # 1 * 10 = 10, which is raised to the minimum fare of 50
    assert base_fare("SL", 10) == 50


def test_unknown_class_raises_error():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("CC", 100)


def test_zero_distance_raises_error():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


# ---------- concession ----------

def test_adult_no_concession():
    assert concession(30, "M", False) == 0


def test_tatkal_gets_no_concession():
    assert concession(3, "M", True) == 0


def test_infant_full_concession():
    assert concession(3, "M", False) == 100


def test_child_half_concession():
    assert concession(10, "F", False) == 50


def test_senior_female_concession():
    assert concession(65, "F", False) == 50


def test_senior_male_concession():
    assert concession(65, "M", False) == 40


# ---------- tatkal_charge ----------

def test_sleeper_tatkal_charge_capped_at_maximum():
    # 5000 // 10 = 500, which is capped at 400
    assert tatkal_charge("SL", 5000) == 400


def test_ac_tatkal_charge_raised_to_minimum():
    # 200 * 3 // 10 = 60, which is raised to 100
    assert tatkal_charge("3A", 200) == 100
