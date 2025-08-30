# eda.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(filename="synthetic_data.csv"):
    # Load dataset
    df = pd.read_csv(filename)
    print("✅ Data loaded successfully!\n")

    # Basic info
    print("📌 Dataset shape:", df.shape)
    print("\n📌 Columns:", df.columns.tolist())
    print("\n📌 Data types:\n", df.dtypes)

    # First few rows
    print("\n📌 Sample data:")
    print(df.head())

    # Missing values check
    print("\n📌 Missing values:\n", df.isnull().sum())

    # Descriptive stats
    print("\n📌 Summary statistics:\n", df.describe())

    # Campaign distribution
    campaign_counts = df["campaign"].value_counts()
    print("\n📌 Campaign counts:\n", campaign_counts)

    # Conversion rates by campaign
    conversion_rates = df.groupby("campaign")["converted"].mean()
    print("\n📌 Conversion rates by campaign:\n", conversion_rates)

    # ------------------- Visualization -------------------
    sns.set(style="whitegrid")

    # Campaign distribution
    plt.figure(figsize=(6,4))
    sns.countplot(x="campaign", data=df, palette="Set2")
    plt.title("Campaign Distribution")
    plt.show()

    # Conversion rate by campaign
    plt.figure(figsize=(6,4))
    sns.barplot(x="campaign", y="converted", data=df, palette="Set1", ci=None)
    plt.title("Conversion Rate by Campaign")
    plt.show()

    # Impressions vs Conversion
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="impression", y="converted", hue="campaign", data=df, alpha=0.6)
    plt.title("Impressions vs Conversion")
    plt.show()

if __name__ == "__main__":
    run_eda()
