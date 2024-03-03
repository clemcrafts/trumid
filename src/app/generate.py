import pandas as pd
import random
import typing
from src.app.config import (
    TEMPERATURE_SAMPLE_MIN,
    TEMPERATURE_SAMPLE_MAX,
    HUMIDITY_SAMPLE_MIN,
    HUMIDITY_SAMPLE_MAX,
    WIND_SPEED_SAMPLE_MIN,
    WIND_SPEED_SAMPLE_MAX)


def generate_test_data(start_at: str = "2024-02-01",
                       end_at: str = "2024-02-08",
                       freq: str = "5T") -> typing.List[dict]:
    """
    Generates a list of dictionaries containing simulated weather data for multiple cities.

    This function creates a list of weather readings for each city within the specified date range
    at the given frequency. Each reading includes temperature, humidity, wind speed, and the timestamp
    of the reading.

    Parameters:
    - start_at (str): The start date of the data generation period in "YYYY-MM-DD" format.
    - end_at (str): The end date of the data generation period in "YYYY-MM-DD" format.
    - freq (str): The frequency of data generation as a pandas date_range frequency string (e.g., '5T' for every 5 minutes).

    Returns:
    - List[dict]: A list of dictionaries where each dictionary represents a weather reading for a city.
                  Each dictionary contains 'city', 'temperature', 'humidity', 'wind_speed', and 'reading_at' keys.

    Example of returned dictionary element:
    {
        'city': 'New York',
        'temperature': 70,
        'humidity': 50,
        'wind_speed': 10,
        'reading_at': '2024-02-01 00:00:00+00:00'
    }
    """
    cities = ["New York", "Los Angeles", "Detroit", "Chicago",
              "San Francisco", "Seattle"]
    df = pd.DataFrame.from_records(
        [
            {
                "city": city,
                "temperature": random.randint(TEMPERATURE_SAMPLE_MIN, TEMPERATURE_SAMPLE_MAX),
                "humidity": random.randint(HUMIDITY_SAMPLE_MIN, HUMIDITY_SAMPLE_MAX),
                "wind_speed": random.randint(WIND_SPEED_SAMPLE_MIN, WIND_SPEED_SAMPLE_MAX),
                "reading_at": ts
            }
            for ts in
            pd.date_range(start_at, end_at, freq=freq, tz="UTC")
            for city in cities
        ]
    )
    return df.to_dict(orient="records")
