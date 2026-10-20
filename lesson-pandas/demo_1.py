import pandas as pd

series = pd.Series([10, 20, 30, 40], name="quantity")
print(series)
print("sum:", series.sum(), "| mean:", series.mean(), "| max:", series.max())

table = pd.DataFrame(
    {
        "product": ["Ноутбук", "Монітор", "Мишка"],
        "price": [32000, 7500, 650],
        "quantity": [1, 2, 10],
    }
)
print(table)
print(table.shape)
print(table["price"] * table["quantity"])
