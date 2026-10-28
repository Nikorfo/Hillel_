import pandas as pd

df = pd.read_csv("sales.csv")

print(df["product"].head(3))
print(df[["product", "price"]].head(3))

print(df.loc[0, "product"])
print(df.loc[0:2, ["product", "price"]])
print(df.iloc[0])
print(df.iloc[0:3, 0:3])

expensive = df[df["price"] > 30000]
print("expensive rows:", len(expensive))

west_laptops = df[(df["region"] == "Захід") & (df["product"] == "Ноутбук")]
print("west laptops:", len(west_laptops))

cheap_or_many = df[(df["price"] < 1000) | (df["quantity"] >= 10)]
print("cheap or many:", len(cheap_or_many))

print(df[df["product"].isin(["Мишка", "Клавіатура"])].shape)
print(df["region"].unique().tolist())
print(df["product"].value_counts())
