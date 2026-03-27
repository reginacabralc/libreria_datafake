from datafake import (
    generate_sales, generate_users, generate_football,
    generate_music, generate_weather, generate_social,
    generate_movies, generate_health, generate_flights,
    generate_elections
)

datasets = {
    "sales": generate_sales(),
    "users": generate_users(),
    "football": generate_football(),
    "music": generate_music(),
    "weather": generate_weather(),
    "social": generate_social(),
    "movies": generate_movies(),
    "health": generate_health(),
    "flights": generate_flights(),
    "elections": generate_elections(),
}

for name, df in datasets.items():
    print(f" {name}: {df.shape} — columnas: {list(df.columns)}")
