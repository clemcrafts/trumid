from app import calculate_rolling_heat_index, store
import pandas as pd
import random
import typing
from datetime import datetime


def run():
    """
    Running the data ingestion application.
    :return:
    """
    print("New batch...")
    result = calculate_rolling_heat_index(generate_test_data())
    store(datetime.now().time(), result)


def generate_test_data(start_at: str = "2024-02-01",
                       end_at: str = "2024-02-08",
                       freq: str = "5T") -> typing.List[dict]:
    cities = ["New York", "Los Angeles", "Detroit", "Chicago",
              "San Francisco", "Seattle"]
    df = pd.DataFrame.from_records(
        [
            {
                "city": city,
                "temperature": random.randint(40, 90),
                "humidity": random.randint(0, 100),
                "wind_speed": random.randint(0, 30),
                "reading_at": ts
            }
            for ts in
            pd.date_range("2024-02-01", "2024-02-08", freq="5T", tz="UTC")
            for city in cities
        ]
    )
    return df.to_dict(orient="records")

if __name__ == '__main__':
    run()