# datafake

A Python library for generating realistic, reproducible, and customizable synthetic datasets.

[![PyPI version](https://badge.fury.io/py/datafake.svg)](https://pypi.org/project/datafake/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

---

## What is datafake?

`datafake` generates plausible synthetic datasets across 10 different domains using real statistical distributions — Poisson, lognormal, Dirichlet, exponential, normal, and more. Every dataset enforces logical consistency between columns, making it suitable for serious use cases.

**Use it for:**
- Testing data pipelines without touching real or sensitive data
- Building dashboards and visualizations during development
- Teaching pandas, SQL, and data analysis with realistic data
- Running machine learning experiments with reproducible inputs
- Generating demos for products before real data is available

---

## Installation

```bash
pip install datafake
```

---

## Quick Start

```python
from datafake import generate_sales

df = generate_sales(n=500, seed=42)
print(df.head())
```

---

## Available Generators

| Generator | Domain | Default rows | Key columns |
|---|---|---|---|
| `generate_sales()` | E-commerce transactions | 500 | date, customer_id, product_id, revenue |
| `generate_users()` | App users & churn | 300 | plan, device, sessions, churned |
| `generate_football()` | Football match stats | 500 | teams, goals, possession, result |
| `generate_music()` | Music streaming | 500 | genre, streams, likes, platform |
| `generate_weather()` | Climate records | 500 | temperature, precipitation, condition |
| `generate_social()` | Social media posts | 500 | likes, reach, engagement_rate |
| `generate_movies()` | Streaming movies | 500 | genre, imdb_score, box_office_usd |
| `generate_health()` | Patient records | 500 | diagnosis, bmi, smoker |
| `generate_flights()` | Flight data | 500 | airline, origin, price_usd, delay_min |
| `generate_elections()` | Fictional elections | 500 | candidate, votes, vote_share_pct |
| `generate_products()` | Product catalog | 50 | category, brand, price, stock |
| `generate_related()` | Customers + Products + Sales | configurable | consistent IDs for joins |
| `generate_custom()` | User-defined schema | configurable | any columns you define |

---

## Parameters

All generators share a common set of optional parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `n` | int | varies | Number of rows to generate |
| `seed` | int | 42 | Random seed for reproducibility |
| `missing_rate` | float | 0.0 | Proportion of NaN values to inject (0.0–1.0) |
| `noise_level` | float | 0.0 | Gaussian noise + outliers on numeric columns (0.0–1.0) |
| `locale` | str | `'en_US'` | Faker locale for text fields (e.g. `'es_MX'`, `'fr_FR'`) |
| `save_to` | str | None | File path to export automatically (`.csv` or `.xlsx`) |

`generate_sales()` and `generate_weather()` also accept `start_date` and `end_date` (YYYY-MM-DD).

---

## Examples

### Inject missing values

```python
df = generate_health(n=500, seed=42, missing_rate=0.2)
print(df.isnull().sum())
# ID and date columns are always protected — they never receive NaNs
```

### Add noise and outliers

```python
df_clean = generate_sales(n=500, seed=42)
df_noisy = generate_sales(n=500, seed=42, noise_level=0.15)
# df_noisy has Gaussian perturbations and ~2% extreme outliers on numeric columns
```

### Change language

```python
df_es = generate_users(n=100, seed=42, locale='es_MX')
df_fr = generate_users(n=100, seed=42, locale='fr_FR')
```

### Export to file

```python
df = generate_sales(n=500, save_to='sales.csv')
df = generate_movies(n=500, save_to='movies.xlsx')
```

### Relational datasets with consistent IDs

```python
from datafake import generate_related

data = generate_related(n_customers=200, n_products=50, n_sales=1000, seed=42)

customers = data['customers']
products  = data['products']
sales     = data['sales']

# IDs are consistent — joins work correctly
merged = sales.merge(customers, on='customer_id').merge(products, on='product_id')
print(merged[['sale_id', 'name', 'segment', 'category', 'revenue']].head())
```

### Custom schema

```python
from datafake import generate_custom

schema = {
    'name':       {'type': 'name'},
    'age':        {'type': 'int', 'min': 18, 'max': 65},
    'salary':     {'type': 'lognormal', 'mean': 10, 'sigma': 0.5},
    'active':     {'type': 'bool', 'p': 0.8},
    'level':      {'type': 'category', 'values': ['Junior', 'Mid', 'Senior'], 'weights': [0.4, 0.4, 0.2]},
    'start_date': {'type': 'date', 'start': '-3y', 'end': 'today'},
}

df = generate_custom(schema, n=500, seed=42)
```

### Dataset summary

```python
from datafake import describe_dataset

df = generate_health(n=500, missing_rate=0.1)
summary = describe_dataset(df)
print(summary)
```

---

## Statistical Distributions

`datafake` uses real statistical distributions to generate plausible data:

| Distribution | Used for |
|---|---|
| **Lognormal** | Prices, streams, likes, box office, votes |
| **Normal** | Temperature, weight, height, IMDb scores |
| **Poisson** | Goals, sessions per month, consultations |
| **Exponential** | Precipitation |
| **Dirichlet** | Vote distribution across candidates |
| **Bernoulli** | Churn, virality, smoker, sequel |
| **Uniform** | Dates, controlled ranges |

---

## Interactive Tutorial

Open the full tutorial notebook directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](COLAB_LINK_HERE)

---

## Docker

```bash
docker build -t datafake .
docker run datafake
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Repository

[https://github.com/reginacabralc/libreria_datafake](https://github.com/reginacabralc/libreria_datafake)

---

## Author

Regina Cabral — [@reginacabralc](https://github.com/reginacabralc)