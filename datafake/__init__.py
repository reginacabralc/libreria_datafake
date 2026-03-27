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
]

__version__ = "0.1.0"