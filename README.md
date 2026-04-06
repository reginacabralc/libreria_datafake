# datafake 🎲

Genera datasets sintéticos realistas para pruebas, enseñanza y desarrollo.

[![PyPI version](https://badge.fury.io/py/datafake.svg)](https://pypi.org/project/datafake/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

---

## ¿Qué es datafake?

`datafake` es una librería de Python que genera datasets sintéticos realistas para 10 dominios distintos. Usa distribuciones estadísticas reales (Poisson, lognormal, Dirichlet, exponencial) para simular comportamientos plausibles con coherencia lógica entre variables.

Ideal para:
- Pruebas de pipelines de datos
- Desarrollo de dashboards sin datos reales
- Enseñanza de pandas, SQL y análisis de datos
- Demos de productos
- Experimentación con modelos de machine learning

---

## Instalación
```bash
pip install datafake
```

---

## Datasets disponibles

| Dataset | Función | Descripción |
|---|---|---|
| Ventas | `generate_sales()` | Transacciones de ecommerce con fechas, productos y montos |
| Usuarios | `generate_users()` | Base de usuarios con plan, dispositivo y churn |
| Fútbol | `generate_football()` | Partidos con equipos, goles y estadísticas |
| Música | `generate_music()` | Canciones con género, streams y plataforma |
| Clima | `generate_weather()` | Registros climáticos con temperatura y precipitación |
| Redes Sociales | `generate_social()` | Posts con likes, comentarios y engagement |
| Películas | `generate_movies()` | Películas con género, plataforma y puntuación de IMDb |
| Salud | `generate_health()` | Pacientes con diagnóstico, signos vitales y BMI |
| Vuelos | `generate_flights()` | Vuelos con aerolínea, origen, destino y precio |
| Elecciones | `generate_elections()` | Resultados electorales ficticios por región |

---

## Uso básico
```python
from datafake import generate_sales

df = generate_sales(n=500, seed=42)
print(df.head())
```
sale_id        date customer_id  ... payment_method     status  revenue
---

## Parámetros disponibles

Todos los generadores aceptan los siguientes parámetros:

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| `n` | int | 500 | Número de filas a generar |
| `seed` | int | 42 | Semilla para reproducibilidad |
| `missing_rate` | float | 0.0 | Proporción de valores faltantes (0.0 a 1.0) |

Los generadores `generate_sales()` y `generate_weather()` también aceptan:

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| `start_date` | str | `"2024-01-01"` | Fecha inicial (YYYY-MM-DD) |
| `end_date` | str | `"2024-12-31"` | Fecha final (YYYY-MM-DD) |

---

## Ejemplos

### Generar múltiples datasets
```python
from datafake import (
    generate_sales, generate_users, generate_football,
    generate_music, generate_weather, generate_social,
    generate_movies, generate_health, generate_flights,
    generate_elections
)

df_sales     = generate_sales()
df_usuarios  = generate_users()
df_futbol    = generate_football()
df_musica    = generate_music()
df_clima     = generate_weather()
df_social    = generate_social()
df_peliculas = generate_movies()
df_salud     = generate_health()
df_vuelos    = generate_flights()
df_elecciones = generate_elections()
```

---

### Controlar el tamaño y la semilla
```python
df = generate_sales(n=1000, seed=99)
print(df.shape)  # (1000, 11)
```

---

### Introducir valores faltantes
```python
df = generate_health(n=500, seed=42, missing_rate=0.2)
print(df.isnull().sum())
```

Las columnas de ID y fechas están protegidas y nunca reciben NaNs.

---

### Reproducibilidad
```python
df1 = generate_sales(seed=42)
df2 = generate_sales(seed=42)
print(df1.equals(df2))  # True
```

---

## Distribuciones estadísticas utilizadas

| Distribución | Dónde se usa |
|---|---|
| **Lognormal** | Precios, streams, likes, taquilla, votos |
| **Normal** | Temperatura, peso, altura, puntuación de IMDb |
| **Poisson** | Goles, sesiones, consultas médicas |
| **Exponencial** | Precipitación |
| **Dirichlet** | Distribución de votos entre candidatos |
| **Bernoulli** | Churn, viralidad, fumador, secuela |
| **Uniforme** | Fechas, rangos controlados |

---

## Tutorial interactivo

Abre el notebook tutorial directamente en Google Colab:

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/reginacabralc/datafake/blob/main/notebooks/tutorial.ipynb)

---

## Instalación con Docker
```bash
docker build -t datafake .
docker run datafake
```

---

## Repositorio

[https://github.com/reginacabralc/datafake](https://github.com/reginacabralc/datafake)

---

## Autora

Regina Cabral — [@reginacabralc](https://github.com/reginacabralc)
