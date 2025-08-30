# analysis.py

import pandas as pd
import numpy as np
from scipy import stats

def run_ab_test(df, group_col="group", outcome_col="converted"):
    """
    Performs A/B test and returns summary as a dict.
    Keys: n_A, n_B, conversions_A, conversions_B, conv_rate_A, conv_rate_B, z_score, p_value
    """
    groups = sorted(df[group_col].unique())
    if "A" not in groups or "B" not in groups:
        raise ValueError("Both A and B groups must be present in the data.")

    # Counts and conversions
    summary = {}
    for g in groups:
        data = df[df[group_col]==g][outcome_col]
        summary[f"n_{g}"] = len(data)
        summary[f"conversions_{g}"] = int(data.sum())
        summary[f"conv_rate_{g}"] = data.mean()

    # Z-test for proportions
    success_a, total_a = summary["conversions_A"], summary["n_A"]
    success_b, total_b = summary["conversions_B"], summary["n_B"]
    p1, p2 = success_a/total_a, success_b/total_b
    p_pool = (success_a + success_b) / (total_a + total_b)
    se = (p_pool*(1-p_pool)*(1/total_a + 1/total_b))**0.5
    z_score = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    summary["z_score"] = z_score
    summary["p_value"] = p_value

    return summary


def compute_confidence_intervals(df, group_col="group", outcome_col="converted", alpha=0.05):
    """
    Computes 95% confidence intervals for conversion rates for A and B.
    Returns dict: {"A": (low, high), "B": (low, high)}
    """
    cis = {}
    for g in ["A", "B"]:
        data = df[df[group_col]==g][outcome_col]
        n = len(data)
        p_hat = data.mean()
        se = np.sqrt(p_hat*(1-p_hat)/n)
        margin = stats.norm.ppf(1 - alpha/2) * se
        cis[g] = (p_hat - margin, p_hat + margin)
    return cis
