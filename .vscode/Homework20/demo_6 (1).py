import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("sales_clean.csv", parse_dates=["date"])

# 1. bar: порівняння категорій
by_region = df.groupby("region")["total"].sum()
by_region.plot(kind="bar", title="Дохід за регіонами", color="steelblue", rot=0)
plt.ylabel("грн")
plt.tight_layout()
plt.savefig("chart_bar.png")
plt.close()

# 2. barh: довгі назви краще читати горизонтально
by_product = df.groupby("product")["total"].sum().sort_values()
by_product.plot(kind="barh", title="Дохід за товарами", color="seagreen")
plt.xlabel("грн")
plt.tight_layout()
plt.savefig("chart_barh.png")
plt.close()

# 3. line: зміна в часі
by_month = df.groupby("month")["total"].sum()
by_month.plot(kind="line", marker="o", title="Дохід за місяцями", grid=True)
plt.xlabel("місяць")
plt.ylabel("грн")
plt.tight_layout()
plt.savefig("chart_line.png")
plt.close()

print("saved: chart_bar.png, chart_barh.png, chart_line.png")
