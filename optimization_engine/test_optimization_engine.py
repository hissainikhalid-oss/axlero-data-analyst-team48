"""
test_optimization_engine.py

Pytest test suite for optimization_engine.py
Covers: correctness of options, constraint enforcement, and
edge cases (infeasible scenarios, zero delay, tight budgets).
"""

import pytest
from optimization_engine import recommend_options


def test_returns_optimal_status_for_normal_case():
    """A reasonable budget and delay tolerance should always find a solution."""
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=20000,
        max_acceptable_delay_days=5,
        base_order_value=100000,
    )
    assert result["status"] == "Optimal"
    assert result["recommended_option"] in ("A", "B", "C")


def test_recommends_air_freight_when_delay_tolerance_is_tight():
    """If almost no delay is acceptable, only Option A (0 days) qualifies."""
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=20000,
        max_acceptable_delay_days=2,   # too tight for B or C
        base_order_value=100000,
    )
    assert result["recommended_option"] == "A"


def test_recommends_cheapest_option_when_delay_tolerance_is_loose():
    """If a long delay is acceptable, the solver should pick the cheapest option (C)."""
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=20000,
        max_acceptable_delay_days=30,  # generous, so cost dominates
        base_order_value=100000,
    )
    assert result["recommended_option"] == "C"
    assert result["options"]["C"]["cost"] == 0


def test_never_exceeds_budget_constraint():
    """The chosen option's cost must never exceed the given budget."""
    budget = 12000
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=budget,
        max_acceptable_delay_days=10,
        base_order_value=100000,
    )
    if result["status"] == "Optimal":
        chosen_cost = result["options"][result["recommended_option"]]["cost"]
        assert chosen_cost <= budget


def test_never_exceeds_delay_constraint():
    """The chosen option's resulting delay must never exceed max_acceptable_delay_days."""
    max_delay = 5
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=20000,
        max_acceptable_delay_days=max_delay,
        base_order_value=100000,
    )
    if result["status"] == "Optimal":
        chosen_delay = result["options"][result["recommended_option"]]["delay_days"]
        assert chosen_delay <= max_delay


def test_infeasible_when_budget_and_delay_both_too_strict():
    """
    If budget is too low for Option A/B and delay tolerance is too low
    for Option C, no option satisfies both constraints -> Infeasible.
    """
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=100,      # too low for A ($15000) or B ($10000)
        max_acceptable_delay_days=1,  # too low for C (14 days)
        base_order_value=100000,
    )
    assert result["status"] == "Infeasible"
    assert result["recommended_option"] is None


def test_all_three_options_always_present_in_output():
    """Regardless of which option is recommended, all 3 should be shown for UI display."""
    result = recommend_options(predicted_delay_days=10)
    assert set(result["options"].keys()) == {"A", "B", "C"}
    for key in ("A", "B", "C"):
        assert "name" in result["options"][key]
        assert "cost" in result["options"][key]
        assert "delay_days" in result["options"][key]
        assert "description" in result["options"][key]


def test_zero_predicted_delay_still_returns_valid_result():
    """Edge case: no delay predicted at all."""
    result = recommend_options(predicted_delay_days=0)
    assert result["status"] == "Optimal"
    assert result["recommended_option"] in ("A", "B", "C")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
