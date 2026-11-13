"""Lab 6 - Code and Branch Coverage tests for pizza_order.py

Student : Dhruv Talavat
SRN     : PES1UG24AM087

This is the completed starter test file: every decision in pizza_order.py is
exercised in both directions, including boundary values, so the module reaches
100% statement and 100% branch coverage.

Run:
    coverage run --branch -m pytest test_pizza_order.py
    coverage report -m
"""

import pytest

from pizza_order import delivery_status, order_discount, pizza_price


# Example test cases (from the starter file):
def test_plain_medium_pizza():
    assert pizza_price("medium", 0, False) == 350


def test_on_time_delivery():
    assert delivery_status(20, 3) == "on time"


# --------------------------------------------------------------------------
# pizza_price
# --------------------------------------------------------------------------
def test_small_pizza_no_toppings():
    assert pizza_price("small", 0, False) == 200


def test_medium_pizza_three_toppings():
    # toppings > 3 is False (boundary: exactly 3)
    assert pizza_price("medium", 3, False) == 350 + 3 * 40


def test_medium_pizza_four_toppings():
    # toppings > 3 is True (boundary: 4, the very next topping)
    assert pizza_price("medium", 4, False) == 350 + 3 * 40 + 1 * 30


def test_large_pizza_extra_toppings():
    assert pizza_price("large", 6, False) == 500 + 3 * 40 + 3 * 30


def test_medium_pizza_with_cheese_burst():
    assert pizza_price("medium", 2, True) == 350 + 2 * 40 + 100


def test_large_pizza_with_cheese_burst():
    assert pizza_price("large", 0, True) == 500 + 100


def test_cheese_burst_small_pizza_raises_value_error():
    with pytest.raises(ValueError):
        pizza_price("small", 2, True)


def test_unknown_size_raises_value_error():
    with pytest.raises(ValueError):
        pizza_price("jumbo", 2, False)


def test_negative_toppings_raises_value_error():
    with pytest.raises(ValueError):
        pizza_price("small", -1, False)


# --------------------------------------------------------------------------
# order_discount
# --------------------------------------------------------------------------
def test_order_below_300_has_no_discount():
    assert order_discount(299, "monday", False) == 0


def test_order_exactly_300_gets_weekday_discount():
    assert order_discount(300, "monday", False) == 30


def test_tuesday_gives_half_price_discount():
    assert order_discount(800, "tuesday", False) == 400


def test_student_tuesday_gets_half_price_plus_50():
    assert order_discount(800, "tuesday", True) == 400 + 50


def test_saturday_has_no_day_discount():
    assert order_discount(600, "saturday", False) == 0


def test_sunday_has_no_day_discount():
    assert order_discount(600, "sunday", False) == 0


def test_student_weekend_still_gets_50():
    assert order_discount(600, "sunday", True) == 50


def test_weekday_gives_ten_percent_discount():
    assert order_discount(500, "monday", False) == 50


def test_student_gets_extra_50_on_weekday():
    assert order_discount(999, "wednesday", True) == 99 + 50


# --------------------------------------------------------------------------
# delivery_status
# --------------------------------------------------------------------------
def test_delivery_exactly_10_km_is_deliverable():
    assert delivery_status(20, 10) == "on time"


def test_delivery_beyond_10_km_is_not_deliverable():
    assert delivery_status(10, 11) == "not deliverable"


def test_delivery_exactly_30_minutes_is_on_time():
    assert delivery_status(30, 5) == "on time"


def test_delivery_31_minutes_is_late():
    assert delivery_status(31, 5) == "late"


def test_delivery_exactly_45_minutes_is_late():
    assert delivery_status(45, 5) == "late"


def test_delivery_46_minutes_is_free_pizza():
    assert delivery_status(46, 5) == "free pizza"
