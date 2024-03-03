import typing

import pandas as pd

C1 = -42.379
C2 = 2.04901523
C3 = 10.14333127
C4 = -0.22475541
C5 = -6.83783 * 1e-3
C6 = -5.481717 * 1e-2
C7 = 1.22874 * 1e-3
C8 = 8.5282 * 1e-4
C9 = -1.99 * 1e-6


def calculate_heat_index(temperature: float, humidity: float) -> float:
    """Calculates heat index using formula from wiki: https://en.wikipedia.org/wiki/Heat_index"""
    return (
        C1
        + C2 * temperature
        + C3 * humidity
        + C4 * temperature * humidity
        + C5 * (temperature**2)
        + C6 * (humidity**2)
        + C7 * (temperature**2) * humidity
        + C8 * (humidity**2) * temperature
        + C9 * (temperature**2) * (humidity**2)
    )


def calculate_rolling_heat_index(
    readings: typing.List[dict], rolling_freq: str = "1D"
) -> typing.List[dict]:
    """
    This function calculates heat index for each raw weather reading.
    Each weather reading record contains fields: "temperature", "humidity", "city" and "reading_at".
    """
    city_readings = {}
    for r in readings:
        crs = city_readings.get(r["city"], [])
        crs.append(r)
        city_readings[r["city"]] = crs
    results = []
    for city, crs in city_readings.items():
        df = pd.DataFrame.from_records(crs)
        df["heat_index"] = df.apply(
            lambda x: calculate_heat_index(x["temperature"], x["humidity"]), axis=1
        )
        rolling_avgs = []
        for _, row in df.iterrows():
            start_at = row["reading_at"] - pd.Timedelta(rolling_freq)
            rolling_avgs.append(
                df[
                    (df["reading_at"] <= row["reading_at"])
                    & (df["reading_at"] >= start_at)
                ]["heat_index"].mean()
            )
        df["rolling_heat_index"] = rolling_avgs
        results.extend(df.to_dict(orient="records"))
    return results
