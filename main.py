# main.py (corrected)

from pathlib import Path
import pandas as pd

from src.data_generator import generate_campaign_data
from src.analysis import run_ab_test, compute_confidence_intervals
from src.optimisation import optimise_budget
from src.visualize import plot_conversion_rates, plot_budget_allocation
from src.report_generator import generate_report

# Paths
DATA_PATH = Path("data/campaigns.csv")
RESULTS_DIR = Path("results")
PLOTS_DIR = RESULTS_DIR / "plots"


def ensure_dirs():
    """Ensure required directories exist."""
    for p in [DATA_PATH.parent, RESULTS_DIR, PLOTS_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def generate_data():
    """Generate synthetic campaign data and save to CSV."""
    df = generate_campaign_data(
        n_samples=8000,
        conv_a=0.055,
        conv_b=0.072,
        save_path=DATA_PATH,
    )
    print("✅ Data generated and saved at", DATA_PATH)
    print(df.head())
    return df


def run_analysis(df):
    """Run A/B test and confidence interval analysis."""
    summary = run_ab_test(df)
    cis = compute_confidence_intervals(df, alpha=0.05)
    print("📊 A/B Test Results:", summary)
    print("📊 Confidence Intervals:", cis)
    return summary, cis


def run_optimisation(summary):
    """Optimise budget allocation based on conversion rates."""
    opt = optimise_budget(
        conv_rate_a=summary["conv_rate_A"],
        conv_rate_b=summary["conv_rate_B"],
        cpi_a=0.025,
        cpi_b=0.03,
        total_budget=10000,
        min_share_each=0.10,
    )

    # Compute expected conversions
    expected_a = opt["allocation"]["A"] / 0.025 * summary["conv_rate_A"]
    expected_b = opt["allocation"]["B"] / 0.03 * summary["conv_rate_B"]
    opt["expected_conversions"] = expected_a + expected_b

    print("📈 Optimal Allocation:", opt)
    return opt


def run_visualisations(summary, cis, opt):
    """Generate plots for conversion rates and budget allocation."""
    plot_conversion_rates(
        conv_a=summary["conv_rate_A"],
        conv_b=summary["conv_rate_B"],
        ci_a=cis["A"],
        ci_b=cis["B"],
        save_path=PLOTS_DIR / "conversion_rates.png",
    )
    plot_budget_allocation(
        allocation=opt["allocation"],
        save_path=PLOTS_DIR / "optimal_allocation.png",
    )
    print("🖼️ Plots saved to", PLOTS_DIR)


def run_report(summary, cis, opt):
    """Generate markdown report of results."""
    report_path = RESULTS_DIR / "report.md"
    generate_report(summary, cis, opt, report_path)
    print("📝 Report generated at", report_path)


def main():
    ensure_dirs()
    df, summary, cis, opt = None, None, None, None

    while True:
        print("\n==== Marketing Campaign Analysis Menu ====")
        print("1. Generate new data")
        print("2. Run A/B test analysis")
        print("3. Run optimisation (budget allocation)")
        print("4. Generate visualisations")
        print("5. Generate report")
        print("6. Run full pipeline")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            df = generate_data()

        elif choice == "2":
            if df is None:
                if DATA_PATH.exists():
                    df = pd.read_csv(DATA_PATH)
                else:
                    print("⚠️ No data found. Generate data first.")
                    continue
            summary, cis = run_analysis(df)

        elif choice == "3":
            if summary is None:
                print("⚠️ Run analysis first (option 2).")
                continue
            opt = run_optimisation(summary)

        elif choice == "4":
            if not (summary and cis and opt):
                print("⚠️ Run analysis + optimisation first.")
                continue
            run_visualisations(summary, cis, opt)

        elif choice == "5":
            if not (summary and cis and opt):
                print("⚠️ Run analysis + optimisation first.")
                continue
            run_report(summary, cis, opt)

        elif choice == "6":
            df = generate_data()
            summary, cis = run_analysis(df)
            opt = run_optimisation(summary)
            run_visualisations(summary, cis, opt)
            run_report(summary, cis, opt)
            print("✅ Full pipeline completed.")

        elif choice == "0":
            print("👋 Exiting. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
