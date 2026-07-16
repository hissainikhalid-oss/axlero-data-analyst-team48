"""
optimization_engine.py

Member-2 Task: SciPy/PuLP optimization, business constraints,
recommendation logic (Option A/B/C), testing.

This module takes a predicted supply-chain disruption (coming from
Member-1's ML model) and business constraints (budget, max delay days,
minimum inventory) and prescribes the best of three options:

  Option A: Air Freight        (fast, expensive)
  Option B: Secondary Supplier (moderate cost & speed, premium price)
  Option C: Delay Launch       (cheapest, slowest)

It uses PuLP to solve a small Mixed-Integer Program: choose exactly
one option that minimizes total cost subject to hard business
constraints (budget ceiling, max acceptable delay).
"""

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpStatus, value


def recommend_options(predicted_delay_days: int,
                       budget_limit: float = 20000,
                       max_acceptable_delay_days: int = 10,
                       base_order_value: float = 100000):
    """
    Given a predicted delay (in days) from the ML model, generate
    Option A/B/C with cost & time trade-offs, then solve for the
    mathematically optimal choice under business constraints.

    Returns a dict with all options (for UI display) and the
    recommended option (from the solver).
    """

    # ---- Step 1: Define the three business options ----
    # These would normally be computed dynamically based on the
    # predicted disruption; here we use representative formulas.
    options = {
        "A": {
            "name": "Air Freight",
            "cost": 15000,
            "delay_days": 0,          # fully resolves the delay
            "description": "Pay premium for air freight to eliminate delay entirely."
        },
        "B": {
            "name": "Secondary Supplier",
            "cost": base_order_value * 0.10,  # 10% premium
            "delay_days": max(0, predicted_delay_days - 7),
            "description": "Source from secondary supplier at a 10% premium."
        },
        "C": {
            "name": "Delay Launch",
            "cost": 0,
            "delay_days": predicted_delay_days,
            "description": "Accept the delay and push back the product launch."
        },
    }

    # ---- Step 2: Build the optimization problem ----
    prob = LpProblem("Supply_Chain_Option_Selection", LpMinimize)

    # Binary decision variable per option: 1 if chosen, 0 otherwise
    choice_vars = {key: LpVariable(f"choose_{key}", cat=LpBinary) for key in options}

    # Objective: minimize total cost of the chosen option
    prob += lpSum(choice_vars[key] * options[key]["cost"] for key in options), "Total_Cost"

    # Constraint: exactly one option must be chosen
    prob += lpSum(choice_vars.values()) == 1, "Choose_Exactly_One"

    # Constraint: cost of chosen option must not exceed budget
    prob += lpSum(choice_vars[key] * options[key]["cost"] for key in options) <= budget_limit, "Budget_Constraint"

    # Constraint: resulting delay must not exceed max acceptable delay
    prob += lpSum(choice_vars[key] * options[key]["delay_days"] for key in options) <= max_acceptable_delay_days, "Delay_Constraint"

    # ---- Step 3: Solve ----
    prob.solve()

    status = LpStatus[prob.status]
    recommended_key = None
    if status == "Optimal":
        for key in options:
            if value(choice_vars[key]) == 1:
                recommended_key = key
                break

    # ---- Step 4: Build result ----
    result = {
        "predicted_delay_days": predicted_delay_days,
        "budget_limit": budget_limit,
        "max_acceptable_delay_days": max_acceptable_delay_days,
        "status": status,
        "options": options,
        "recommended_option": recommended_key,
    }
    return result


if __name__ == "__main__":
    # Example run, mirroring the "Supply Prescript" use case from the
    # project document: a 14-day predicted delay for microchips.
    result = recommend_options(
        predicted_delay_days=14,
        budget_limit=20000,
        max_acceptable_delay_days=5,
        base_order_value=100000,
    )

    print("Solver status:", result["status"])
    print("\nAll options evaluated:")
    for key, opt in result["options"].items():
        print(f"  Option {key} - {opt['name']}: cost=${opt['cost']:.0f}, "
              f"delay={opt['delay_days']} days")

    print(f"\nRecommended option: {result['recommended_option']} "
          f"({result['options'][result['recommended_option']]['name']})")
