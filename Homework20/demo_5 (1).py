import pandas as pd

df = pd.read_csv("sales_clean.csv")

fact = df.groupby("region")["total"].sum().round(0).reset_index()
plans = pd.read_csv("plans.csv")
print(fact)
print(plans)

merged = fact.merge(plans, on="region")
merged["done_percent"] = (merged["total"] / merged["plan"] * 100).round(1)
merged["diff"] = (merged["total"] - merged["plan"]).round(0)
print(merged.sort_values("done_percent", ascending=False))
