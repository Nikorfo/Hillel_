import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("sales_clean.csv", parse_dates=["date"])

sns.set_theme(style="whitegrid")

sns.barplot(data=df, x="region", y="total", estimator="sum", errorbar=None, hue="region")
plt.title("Дохід за регіонами (seaborn)")
plt.tight_layout()
plt.savefig("chart_seaborn.png")
plt.close()

sns.boxplot(data=df, x="product", y="total")
plt.title("Розкид сум замовлень по товарах")
plt.tight_layout()
plt.savefig("chart_box.png")
plt.close()

print("saved chart_seaborn.png, chart_box.png")
