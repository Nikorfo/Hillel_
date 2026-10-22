import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("sales_clean.csv", parse_dates=["date"])

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Продажі 2026", fontsize=14)

df.groupby("region")["total"].sum().plot(kind="bar", ax=axes[0, 0], title="Дохід за регіонами", rot=0)
df.groupby("month")["total"].sum().plot(kind="line", marker="o", ax=axes[0, 1], title="Дохід за місяцями")
df.groupby("product")["total"].sum().sort_values().plot(kind="barh", ax=axes[1, 0], title="Дохід за товарами")
df["product"].value_counts().plot(kind="pie", ax=axes[1, 1], ylabel="", title="Кількість замовлень")

plt.tight_layout()
plt.savefig("dashboard.png", dpi=120)
plt.close()
print("saved dashboard.png")
