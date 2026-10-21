import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("sales_clean.csv", parse_dates=["date"])

by_seller = df.groupby("seller")["total"].sum().sort_values(ascending=False)

by_seller.to_csv("sellers.csv")
by_seller.plot(kind="bar", title="Дохід за продавцями", color="steelblue", rot=0)
plt.ylabel("грн")
plt.tight_layout()
plt.savefig("sellers.png")
plt.close()

print(by_seller.round(2))
print("saved: sellers.csv, sellers.png")

