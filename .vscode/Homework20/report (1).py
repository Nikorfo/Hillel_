# pandas: код двох занять

Одна тема, розбита на два заняття. Проєкт один, файли йдуть по порядку.

## Запуск

```bash
uv sync
uv run demo_1.py
```

Запускати з папки проєкту: скрипти читають `sales.csv` із поточної теки.

## Заняття 1 — таблиці, читання, вибірка

| Файл | Про що |
|------|--------|
| `demo_1.py` | `Series` і `DataFrame`, операції над колонкою без циклу |
| `demo_2.py` | `read_csv`, `head`, `shape`, `columns`, `dtypes`, `info`, `describe` |
| `demo_3.py` | вибірка `df["col"]`, `loc`, `iloc`; фільтри, `&`, `|`, `isin`, `unique` |

## Заняття 2 — чищення, групування, графіки

| Файл | Про що |
|------|--------|
| `demo_4.py` | чищення: `isna`, `drop_duplicates`, `fillna`, `astype`, `.str`, `to_datetime`; створює `sales_clean.csv` |
| `demo_5.py` | `groupby`, `agg`, `pivot_table`, `nlargest` |
| `demo_6.py` | `merge`: факт проти плану (`plans.csv`) |
| `demo_7.py` | графіки `bar`, `barh`, `line` |
| `demo_8.py` | графіки `pie`, `hist`, `scatter`, кілька ліній |
| `demo_9.py` | дашборд: чотири графіки на одній картинці |
| `demo_10.py` | `seaborn`: `barplot`, `boxplot` |
| `report.py` | усе разом + `argparse`: `uv run report.py --region Захід` |

**`demo_4.py` запускати першим із цієї групи:** решта читають `sales_clean.csv`,
який він створює.

## Дані

- `sales.csv` — 202 рядки продажів, навмисно «брудні»: пропуски в `quantity`,
  2 дублікати, різні написання регіонів (`Захід` і `захід`);
- `plans.csv` — план продажів на регіон.

Перевірено: Python 3.14.7, pandas 3.0.6, matplotlib 3.11.2, seaborn 0.13.2.
