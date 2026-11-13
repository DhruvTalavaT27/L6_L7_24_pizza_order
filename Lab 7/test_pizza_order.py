"""Lab 7 - Fuzz testing pizza_order.py with Hypothesis

Student : Dhruv Talavat
SRN     : PES1UG24AM087

Step 3 of the handout: use Hypothesis to uncover edge cases automatically for
all three functions (toppings_price, pizza_inches, split_bill).  Each property
follows the handout pattern - the function is called inside try/except and any
exception is reported as a failure - so the fuzzer stops at the first input
that crashes the application.

Run:
    python -m pytest test_pizza_order.py
"""

import pytest
from hypothesis import given, strategies as st

from pizza_order import SIZES, pizza_inches, split_bill, toppings_price


# --------------------------------------------------------------------------
# Fuzz tests: no input, however malformed, may crash the application
# --------------------------------------------------------------------------
@given(st.text() | st.none())
def test_toppings_price_no_crash(s):
    try:
        result = toppings_price(s)
    except Exception as e:
        assert False, f"toppings_price crashed with: {e!r}"
    assert isinstance(result, int)
    assert result >= 0


@given(st.text() | st.none())
def test_pizza_inches_no_crash(s):
    try:
        result = pizza_inches(s)
    except Exception as e:
        assert False, f"pizza_inches crashed with: {e!r}"
    assert isinstance(result, int)
    assert result in set(SIZES.values()) | {0}


@given(st.text() | st.none())
def test_split_bill_no_crash(s):
    try:
        result = split_bill(s)
    except Exception as e:
        assert False, f"split_bill crashed with: {e!r}"
    assert isinstance(result, float)
    assert result >= 0


# --------------------------------------------------------------------------
# Regression tests for the crashes Hypothesis found while fuzzing
# --------------------------------------------------------------------------
@pytest.mark.parametrize("value", [None, "", "   ", ",", ",,", "chicken"])
def test_toppings_price_rejects_junk_without_crashing(value):
    assert toppings_price(value) == 0


@pytest.mark.parametrize("value", [None, "", "XL", "small", "12"])
def test_pizza_inches_unknown_size_returns_zero(value):
    assert pizza_inches(value) == 0


@pytest.mark.parametrize("value", [None, "", "abc", "900", "900/0", "900/0/3", "-900/3"])
def test_split_bill_unparseable_input_returns_zero(value):
    assert split_bill(value) == 0.0


# --------------------------------------------------------------------------
# The fixed functions must still be correct for valid input
# --------------------------------------------------------------------------
def test_toppings_price_sums_known_toppings():
    assert toppings_price("cheese,olives") == 70


def test_toppings_price_ignores_case_and_spaces():
    assert toppings_price("  CHEESE , Paneer ") == 90


def test_pizza_inches_accepts_lower_case():
    assert pizza_inches("m") == 10


def test_pizza_inches_trims_spaces():
    assert pizza_inches(" L ") == 12


def test_split_bill_divides_exactly():
    assert split_bill("900/3") == 300.0


def test_split_bill_rounds_to_two_decimals():
    assert split_bill("1000/3") == 333.33


def test_split_bill_allows_surrounding_spaces():
    assert split_bill(" 900 / 4 ") == 225.0
