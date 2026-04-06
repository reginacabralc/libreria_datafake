import pytest
import pandas as pd
from datafake import (
    generate_sales, generate_users, generate_football,
    generate_music, generate_weather, generate_social,
    generate_movies, generate_health, generate_flights,
    generate_elections
)

# Pruebas de tamaño

def test_sales_shape():
    df = generate_sales(n=100)
    assert df.shape[0] == 100

def test_users_shape():
    df = generate_users(n=50)
    assert df.shape[0] == 50

def test_football_shape():
    df = generate_football(n=200)
    assert df.shape[0] == 200

def test_music_shape():
    df = generate_music(n=300)
    assert df.shape[0] == 300

def test_weather_shape():
    df = generate_weather(n=150)
    assert df.shape[0] == 150

def test_social_shape():
    df = generate_social(n=100)
    assert df.shape[0] == 100

def test_movies_shape():
    df = generate_movies(n=100)
    assert df.shape[0] == 100

def test_health_shape():
    df = generate_health(n=100)
    assert df.shape[0] == 100

def test_flights_shape():
    df = generate_flights(n=100)
    assert df.shape[0] == 100

def test_elections_shape():
    df = generate_elections(n=100)
    assert df.shape[0] == 100

# Pruebas de tipo de retorno

def test_all_return_dataframe():
    assert isinstance(generate_sales(), pd.DataFrame)
    assert isinstance(generate_users(), pd.DataFrame)
    assert isinstance(generate_football(), pd.DataFrame)
    assert isinstance(generate_music(), pd.DataFrame)
    assert isinstance(generate_weather(), pd.DataFrame)
    assert isinstance(generate_social(), pd.DataFrame)
    assert isinstance(generate_movies(), pd.DataFrame)
    assert isinstance(generate_health(), pd.DataFrame)
    assert isinstance(generate_flights(), pd.DataFrame)
    assert isinstance(generate_elections(), pd.DataFrame)

# Pruebas de reproducibilidad

def test_sales_reproducibility():
    df1 = generate_sales(seed=42)
    df2 = generate_sales(seed=42)
    assert df1.equals(df2)

def test_users_reproducibility():
    df1 = generate_users(seed=42)
    df2 = generate_users(seed=42)
    assert df1.equals(df2)

def test_football_reproducibility():
    df1 = generate_football(seed=42)
    df2 = generate_football(seed=42)
    assert df1.equals(df2)

def test_music_reproducibility():
    df1 = generate_music(seed=42)
    df2 = generate_music(seed=42)
    assert df1.equals(df2)

def test_weather_reproducibility():
    df1 = generate_weather(seed=42)
    df2 = generate_weather(seed=42)
    assert df1.equals(df2)

# Pruebas de valores faltantes

def test_no_missing_by_default():
    for df in [
        generate_sales(), generate_users(), generate_football(),
        generate_music(), generate_weather(), generate_social(),
        generate_movies(), generate_health(), generate_flights(),
        generate_elections()
    ]:
        assert df.isnull().sum().sum() == 0

def test_missing_rate_injects_nans():
    df = generate_sales(n=500, missing_rate=0.2)
    assert df.isnull().sum().sum() > 0

def test_missing_rate_protects_ids():
    df = generate_sales(n=500, missing_rate=0.5)
    assert df["sale_id"].isnull().sum() == 0
    assert df["customer_id"].isnull().sum() == 0
    assert df["product_id"].isnull().sum() == 0

def test_missing_rate_protects_dates():
    df = generate_sales(n=500, missing_rate=0.5)
    assert df["date"].isnull().sum() == 0

def test_invalid_missing_rate_raises_error():
    with pytest.raises(ValueError):
        generate_sales(missing_rate=1.5)

# Pruebas de columnas

def test_sales_columns():
    df = generate_sales()
    expected = ["sale_id", "date", "customer_id", "product_id",
                "category", "quantity", "unit_price", "payment_method",
                "status", "store", "revenue"]
    assert list(df.columns) == expected

def test_health_has_bmi():
    df = generate_health()
    assert "bmi" in df.columns

def test_users_has_churned():
    df = generate_users()
    assert "churned" in df.columns
    assert df["churned"].isin([0, 1]).all()

def test_football_possession_sums_100():
    df = generate_football()
    total = (df["home_possession"] + df["away_possession"]).round(1)
    assert (total == 100.0).all()

def test_sales_revenue_is_correct():
    df = generate_sales()
    expected_revenue = (df["quantity"] * df["unit_price"]).round(2)
    assert (df["revenue"] == expected_revenue).all()

def test_social_engagement_rate():
    df = generate_social()
    assert "engagement_rate" in df.columns
    assert (df["engagement_rate"] >= 0).all()

def test_elections_vote_share():
    df = generate_elections()
    assert "vote_share_pct" in df.columns
    assert (df["vote_share_pct"] >= 0).all()
    assert (df["vote_share_pct"] <= 100).all()