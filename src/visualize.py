from pathlib import Path
import matplotlib.pyplot as plt

def plot_conversion_rates(conv_a, conv_b, ci_a, ci_b, save_path: Path):
    labels = ["A", "B"]
    values = [conv_a, conv_b]
    errors = [
        [values[0] - ci_a[0], ci_a[1] - values[0]],
        [values[1] - ci_b[0], ci_b[1] - values[1]],
    ]

    fig = plt.figure()
    plt.bar(labels, values, yerr=[[e[0] for e in errors], [e[1] for e in errors]], capsize=8, color=['#4C72B0','#55A868'])
    plt.ylabel("Conversion rate")
    plt.title("Observed Conversion Rates (95% CI)")
    plt.ylim(0, max(values)*1.4)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close(fig)

def plot_budget_allocation(allocation: dict, save_path: Path):
    labels = list(allocation.keys())
    sizes = list(allocation.values())
    fig = plt.figure()
    if sum(sizes) == 0:
        plt.text(0.5, 0.5, "No allocation (0 budget)", ha="center", va="center")
    else:
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=['#4C72B0','#55A868'])
        plt.title("Optimal Budget Allocation")
    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=200)
    plt.close(fig)

def plot_revenue(df, group_col="group", revenue_col="revenue", save_path: Path=None):
    """
    New function: Plot total revenue per campaign
    """
    revenue = df.groupby(group_col)[revenue_col].sum()
    fig = plt.figure()
    revenue.plot(kind='bar', color=['#4C72B0','#55A868'])
    plt.ylabel("Total Revenue ($)")
    plt.title("Total Revenue by Campaign")
    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200)
    plt.show()
    plt.close(fig)
