# cada import importa una función de su archivo correspondiente (con el . busca dentro del propio archivo)
from .sales import generate_sales
from .users import generate_users
from .football import generate_football
from .music import generate_music
from .weather import generate_weather
from .social import generate_social
from .movies import generate_movies
from .health import generate_health
from .flights import generate_flights
from .elections import generate_elections
from .products import generate_products
from .related import generate_related
from .utils import inject_missing, export_data, describe_dataset

# define las funciones públicas (lo que se exporta cuando alguien hace from datafake import *)
__all__ = [
    "generate_sales",
    "generate_users",
    "generate_football",
    "generate_music",
    "generate_weather",
    "generate_social",
    "generate_movies",
    "generate_health",
    "generate_flights",
    "generate_elections",
    "generate_products",
    "generate_related",
    "describe_dataset",
]

# guarda la versión de la librería (debe coincidir siempre con la versión en pyproject.toml)
__version__ = "0.2.0"