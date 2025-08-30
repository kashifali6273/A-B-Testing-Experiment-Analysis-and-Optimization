# src/optimisation.py (corrected)

import pulp

def optimise_budget(conv_rate_a: float, conv_rate_b: float, cpi_a: float, cpi_b: float,
                    total_budget: float, min_share_each: float = 0.0):
    """
    Linear program to maximise expected conversions given conversion rates and CPIs.
    """
    prob = pulp.LpProblem("BudgetAllocation", pulp.LpMaximize)

    # Decision variables: spend on A and B
    x_A = pulp.LpVariable("x_A", lowBound=0)
    x_B = pulp.LpVariable("x_B", lowBound=0)

    # Conversion efficiency per unit budget
    efficiency_a = conv_rate_a / cpi_a
    efficiency_b = conv_rate_b / cpi_b

    # Objective: maximise expected conversions
    prob += efficiency_a * x_A + efficiency_b * x_B

    # Budget constraint
    prob += x_A + x_B <= total_budget, "Budget"

    # Optional min-share constraints
    if min_share_each > 0:
        prob += x_A >= min_share_each * total_budget
        prob += x_B >= min_share_each * total_budget

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Get allocations
    allocation = {"A": x_A.value(), "B": x_B.value()}

    # Compute expected conversions
    expected_conversions = allocation["A"] / cpi_a * conv_rate_a + allocation["B"] / cpi_b * conv_rate_b

    return {
        "allocation": allocation,
        "total_budget": total_budget,
        "cpi_a": cpi_a,
        "cpi_b": cpi_b,
        "efficiency_a": efficiency_a,
        "efficiency_b": efficiency_b,
        "expected_conversions": expected_conversions,
        "status": pulp.LpStatus[prob.status],
    }
