import pandas as pd

df = pd.read_csv("sales.csv")
print("start:", df.shape)

print(df.isna().sum())
print("duplicates:", df.duplicated().sum())

df = df.drop_duplicates()
df["quantity"] = df["quantity"].fillna(1).astype(int)
df["region"] = df["region"].str.strip().str.capitalize()
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month
df["total"] = df["quantity"] * df["price"]
df = df.rename(columns={"manager": "seller"})

print("after cleaning:", df.shape)
print("regions:", df["region"].unique().tolist())
print(df.head(3))

df.to_csv("sales_clean.csv", index=False)
print("saved sales_clean.csv")
