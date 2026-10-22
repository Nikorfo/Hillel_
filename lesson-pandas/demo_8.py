import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("sales_clean.csv", parse_dates=["date"])

# 4. pie: частка кожного товару в доході
by_product = df.groupby("product")["total"].sum()
by_product.plot(kind="pie", autopct="%1.1f%%", ylabel="", title="Частка товарів у доході")
plt.tight_layout()
plt.savefig("chart_pie.png")
plt.close()

# 5. hist: як розподілені суми замовлень
df["total"].plot(kind="hist", bins=20, title="Розподіл сум замовлень", color="darkorange")
plt.xlabel("сума замовлення, грн")
plt.tight_layout()
plt.savefig("chart_hist.png")
plt.close()

# 6. scatter: чи є зв'язок між ціною і кількістю
df.plot(kind="scatter", x="price", y="quantity", alpha=0.5, title="Ціна і кількість")
plt.tight_layout()
plt.savefig("chart_scatter.png")
plt.close()

# 7. кілька ліній на одному графіку
pivot = df.pivot_table(index="month", columns="product", values="total", aggfunc="sum")
pivot.plot(kind="line", marker="o", figsize=(9, 5), title="Дохід за місяцями по товарах")
plt.ylabel("грн")
plt.legend(title="товар")
plt.tight_layout()
plt.savefig("chart_multi.png")
plt.close()

print("saved: chart_pie.png, chart_hist.png, chart_scatter.png, chart_multi.png")
