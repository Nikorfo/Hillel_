import argparse

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load(path):
    df = pd.read_csv(path)
    df = df.drop_duplicates()
    df["quantity"] = df["quantity"].fillna(1).astype(int)
    df["region"] = df["region"].str.strip().str.capitalize()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["total"] = df["quantity"] * df["price"]
    return df.rename(columns={"manager": "seller"})


def print_report(df):
    print(f"замовлень: {len(df)}")
    print(f"дохід: {df['total'].sum():,.2f} грн")
    print(f"середній чек: {df['total'].mean():,.2f} грн")
    print("\nдохід за товарами:")
    print(df.groupby("product")["total"].sum().sort_values(ascending=False).round(2))
    print(f"\nнайкращий місяць: {df.groupby('month')['total'].sum().idxmax()}")


def plan_vs_fact(df, plans_path):
    fact = df.groupby("region")["total"].sum().reset_index()
    plans = pd.read_csv(plans_path)
    merged = fact.merge(plans, on="region")
    merged["done_percent"] = (merged["total"] / merged["plan"] * 100).round(1)
    print("\nвиконання плану, %:")
    print(merged[["region", "done_percent"]].sort_values("done_percent", ascending=False).to_string(index=False))
    return merged


def make_dashboard(df, merged, path):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Звіт з продажів", fontsize=14)

    df.groupby("month")["total"].sum().plot(kind="line", marker="o", ax=axes[0, 0], title="Дохід за місяцями")
    df.groupby("product")["total"].sum().sort_values().plot(kind="barh", ax=axes[0, 1], title="Дохід за товарами")
    df.groupby("seller")["total"].sum().plot(kind="bar", ax=axes[1, 0], title="Дохід за продавцями", rot=0)
    merged.set_index("region")["done_percent"].plot(
        kind="bar", ax=axes[1, 1], title="Виконання плану, %", rot=0, color="seagreen"
    )
    axes[1, 1].axhline(100, color="red", linestyle="--")

    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"\nграфіки збережено: {path}")


def main():
    parser = argparse.ArgumentParser(description="Sales report with charts")
    parser.add_argument("--path", default="sales.csv")
    parser.add_argument("--plans", default="plans.csv")
    parser.add_argument("--out", default="dashboard.png")
    parser.add_argument("--region", default=None)
    args = parser.parse_args()

    all_data = load(args.path)

    df = all_data
    if args.region:
        df = all_data[all_data["region"] == args.region]
        print(f"регіон: {args.region}")

    print_report(df)
    merged = plan_vs_fact(all_data, args.plans)
    make_dashboard(df, merged, args.out)


if __name__ == "__main__":
    main()
