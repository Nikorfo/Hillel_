import pandas as pd

df = pd.read_csv("sales_clean.csv", parse_dates=["date"])

print("дохід:", round(df["total"].sum(), 2))
print("середній чек:", round(df["total"].mean(), 2))

print(df.groupby("region")["total"].sum().round(0))

print(
    df.groupby("product").agg(
        orders=("total", "count"),
        revenue=("total", "sum"),
        avg_price=("price", "mean"),
    ).round(2)
)

print(df.groupby(["region", "product"])["total"].sum().round(0).head(6))

print(df.pivot_table(index="region", columns="product", values="total", aggfunc="sum").round(0))

print(df.nlargest(3, "total")[["date", "seller", "product", "total"]])
