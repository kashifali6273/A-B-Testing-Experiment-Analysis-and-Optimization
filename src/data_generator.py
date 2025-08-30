import pandas as pd
import numpy as np
import os

def generate_campaign_data(
    n_samples=10000,
    conv_a=0.05,
    conv_b=0.07,
    save_path="data/campaigns.csv",
    revenue_per_conversion_a=100,  # revenue if user converts in A
    revenue_per_conversion_b=120   # revenue if user converts in B
):
    np.random.seed(42)

    # Simulate demographics
    age = np.random.randint(18, 65, n_samples)
    income = np.random.randint(2000, 10000, n_samples)
    region = np.random.choice(["Urban", "Rural"], size=n_samples)

    # Assign campaigns randomly
    campaigns = np.random.choice(["A", "B"], size=n_samples)

    # Impressions and ad spend
    impressions = np.random.binomial(1, 0.7, n_samples)
    ad_spend = np.round(np.random.uniform(1, 10, n_samples), 2)

    # Conversions
    conversions = []
    revenue = []
    for camp, imp in zip(campaigns, impressions):
        if camp == "A":
            conv = np.random.binomial(1, conv_a if imp else 0.01)
            conversions.append(conv)
            revenue.append(conv * revenue_per_conversion_a)
        else:
            conv = np.random.binomial(1, conv_b if imp else 0.01)
            conversions.append(conv)
            revenue.append(conv * revenue_per_conversion_b)

    # Build DataFrame
    df = pd.DataFrame({
        "user_id": np.arange(1, n_samples + 1),
        "campaign": campaigns,
        "group": campaigns,   # for compatibility
        "age": age,
        "income": income,
        "region": region,
        "impression": impressions,
        "ad_spend": ad_spend,
        "converted": conversions,
        "revenue": revenue,
    })

    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save dataset
    df.to_csv(save_path, index=False)
    return df
