# ab_test.py (corrected version)

import pandas as pd
from scipy import stats

def run_analysis(df):
    """
    Runs analysis and returns a summary dictionary + confidence intervals.
    """

    # Group by campaign
    grouped = df.groupby("campaign")["converted"]
    conversion_rates = grouped.mean()

    # Summary table
    summary = df.groupby("campaign")["converted"].agg(["sum", "count"])
    summary["failures"] = summary["count"] - summary["sum"]
    summary["conv_rate"] = summary["sum"] / summary["count"]

    print("📌 Conversion rates by campaign:\n", conversion_rates)
    print("\n📌 Campaign conversion summary:\n", summary)

    results = {}
    cis = {}

    if "A" in summary.index and "B" in summary.index:
        # Extract values
        success_a, total_a = summary.loc["A", ["sum", "count"]]
        success_b, total_b = summary.loc["B", ["sum", "count"]]

        p1, p2 = success_a / total_a, success_b / total_b
        p_pool = (success_a + success_b) / (total_a + total_b)
        se = (p_pool * (1 - p_pool) * (1/total_a + 1/total_b)) ** 0.5
        z_score = (p1 - p2) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        # Save results in dict
        results = {
            "conv_rate_a": p1,
            "conv_rate_b": p2,
            "z_score": z_score,
            "p_value": p_value
        }

        # Confidence Intervals
        ci_a = stats.norm.interval(0.95, loc=p1, scale=(p1*(1-p1)/total_a)**0.5)
        ci_b = stats.norm.interval(0.95, loc=p2, scale=(p2*(1-p2)/total_b)**0.5)

        cis = {"A": ci_a, "B": ci_b}

        print("\n📊 A/B Test: Campaign A vs Campaign B")
        print(f"Conversion A: {p1:.3f}, Conversion B: {p2:.3f}")
        print(f"Z-score: {z_score:.3f}, P-value: {p_value:.4f}")

        if p_value < 0.05:
            print("✅ Statistically significant difference!")
        else:
            print("❌ No significant difference (could be random chance).")

    else:
        print("⚠️ Both A and B must be present for the test.")

    return results, cis
