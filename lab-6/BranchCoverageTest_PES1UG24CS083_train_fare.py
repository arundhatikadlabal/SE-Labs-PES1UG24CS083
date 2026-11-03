"""Test cases for branch coverage of train_fare.py.

Every decision in train_fare.py is tested for both its True and False
outcome, including the boundary values of each condition.
"""
import pytest
from train_fare import base_fare, concession, tatkal_charge


# ---------- base_fare ----------
# Decisions: class valid?  distance <= 0?  fare < 50?

def test_unknown_class_raises_error():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("CC", 100)


def test_zero_distance_raises_error():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


def test_negative_distance_raises_error():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("2A", -5)


def test_fare_below_minimum_is_raised():
    # fare < 50 is True
    assert base_fare("SL", 10) == 50


def test_fare_exactly_at_minimum_is_unchanged():
    # fare < 50 is False at the boundary
    assert base_fare("SL", 50) == 50


@pytest.mark.parametrize("travel_class, expected", [
    ("SL", 500),
    ("3A", 1000),
    ("2A", 1500),
    ("1A", 2500),
])
def test_fare_for_every_class(travel_class, expected):
    # fare < 50 is False
    assert base_fare(travel_class, 500) == expected


# ---------- concession ----------
# Decisions: tatkal?  age < 5?  age <= 12?  age >= 60?  gender == "F"?

def test_tatkal_gets_no_concession():
    assert concession(70, "F", True) == 0


def test_infant_full_concession():
    assert concession(4, "M", False) == 100


def test_age_five_is_a_child():
    # age < 5 is False, age <= 12 is True
    assert concession(5, "M", False) == 50


def test_age_twelve_is_a_child():
    assert concession(12, "F", False) == 50


def test_age_thirteen_gets_no_concession():
    # age <= 12 is False, age >= 60 is False
    assert concession(13, "M", False) == 0


def test_age_fifty_nine_gets_no_concession():
    assert concession(59, "F", False) == 0


def test_senior_female_at_sixty():
    # age >= 60 is True, gender == "F" is True
    assert concession(60, "F", False) == 50


def test_senior_male_at_sixty():
    # age >= 60 is True, gender == "F" is False
    assert concession(60, "M", False) == 40


# ---------- tatkal_charge ----------
# Decisions: class == "SL"?  charge > 400?  charge < 100?

def test_sleeper_charge_within_limits():
    # SL branch, charge between 100 and 400
    assert tatkal_charge("SL", 2000) == 200


def test_ac_charge_within_limits():
    # non-SL branch, charge between 100 and 400
    assert tatkal_charge("2A", 1000) == 300


def test_charge_capped_at_maximum():
    # charge > 400 is True
    assert tatkal_charge("1A", 2000) == 400


def test_charge_exactly_at_maximum_is_unchanged():
    # charge > 400 is False at the boundary
    assert tatkal_charge("SL", 4000) == 400


def test_charge_raised_to_minimum():
    # charge < 100 is True
    assert tatkal_charge("SL", 500) == 100


def test_charge_exactly_at_minimum_is_unchanged():
    # charge < 100 is False at the boundary
    assert tatkal_charge("SL", 1000) == 100
