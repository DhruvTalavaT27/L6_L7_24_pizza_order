"""Lab 6 - Code Coverage test cases for pizza_order.py

Student : Dhruv Talavat
SRN     : PES1UG24AM087

Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM087_pizza_order.py
    coverage report -m
"""

import pytest

from pizza_order import delivery_status, order_discount, pizza_price


# --------------------------------------------------------------------------
# pizza_price: size / topping / cheese burst pricing
# --------------------------------------------------------------------------
def test_small_pizza_no_toppings():
    assert pizza_price("small", 0, False) == 200


def test_medium_pizza_three_toppings():
    # toppings > 3 is False, so each topping costs 40
    assert pizza_price("medium", 3, False) == 350 + 3 * 40


def test_large_pizza_extra_toppings():
    # first 3 toppings at 40, every extra topping at 30
    assert pizza_price("large", 5, False) == 500 + 3 * 40 + 2 * 30


def test_medium_pizza_with_cheese_burst():
    assert pizza_price("medium", 2, True) == 350 + 2 * 40 + 100


def test_unknown_size_raises_value_error():
    with pytest.raises(ValueError):
        pizza_price("jumbo", 2, False)


def test_negative_toppings_raises_value_error():
    with pytest.raises(ValueError):
        pizza_price("small", -1, False)


# --------------------------------------------------------------------------
# order_discount: day based discount and student bonus
# --------------------------------------------------------------------------
def test_order_below_300_has_no_discount():
    assert order_discount(250, "monday", False) == 0


def test_tuesday_gives_half_price_discount():
    assert order_discount(800, "tuesday", False) == 400


def test_weekend_has_no_day_discount():
    assert order_discount(600, "saturday", False) == 0


def test_student_gets_extra_50_on_weekday():
    assert order_discount(500, "monday", True) == 50 + 50


# --------------------------------------------------------------------------
# delivery_status: distance limit and delivery time
# --------------------------------------------------------------------------
def test_on_time_delivery():
    assert delivery_status(20, 3) == "on time"


def test_late_delivery():
    assert delivery_status(40, 7) == "late"


def test_delivery_beyond_10_km_is_not_deliverable():
    assert delivery_status(10, 12) == "not deliverable"
