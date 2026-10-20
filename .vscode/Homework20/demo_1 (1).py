import pandas as pd

df = pd.read_csv("sales.csv")

print(df.head())
print("rows, columns:", df.shape)
print(df.columns.tolist())
print(df.dtypes)
df.info()
print(df.describe())
