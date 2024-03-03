from .config import C1, C2, C3, C4, C5, C6, C7, C8, C9
import pandas as pd
import numpy as np
import typing


def calculate_rolling_heat_index_optimized(readings: typing.List[dict],
                                           rolling_freq: str = "1D") -> typing.List[dict]:
    """
    Calculate the rolling heat index for a list of temperature and humidity
    readings.

    Parameters:
    - readings (List[dict]): A list of dictionaries, each containing 'city',
    'reading_at', 'temperature', and 'humidity'.
    - rolling_freq (str): A string specifying the frequency for rolling
    calculation (default is "1D" for one day).

    Returns:
    - List[dict]: A list of dictionaries with original data and added
    'heat_index' and 'rolling_heat_index' values.
    """
    # Convert readings to DataFrame
    df = pd.DataFrame(readings)

    # Ensure 'reading_at' is a datetime type and set as the index
    df['reading_at'] = pd.to_datetime(df['reading_at'])
    df.set_index('reading_at', inplace=True)

    df['temperature'] = df['temperature'].astype('float32')
    df['humidity'] = df['humidity'].astype('float32')

    df['heat_index'] = calculate_heat_index_optimized(df['temperature'], df['humidity'])
    df['rolling_heat_index'] = df.groupby('city')['heat_index'] \
        .transform(lambda x: x.rolling(rolling_freq, closed='both').mean())
    df.reset_index(inplace=True)
    return df.to_dict('records')


def calculate_heat_index_optimized(temperature: np.ndarray, humidity: np.ndarray) -> np.ndarray:
    """
    Vectorized version of heat index calculation, optimized with pre-calculated squares.

    This function calculates the heat index based on temperature and humidity using
    the formula with coefficients from the config module. It is optimized for performance
    by pre-calculating squares and products of temperature and humidity.

    Parameters:
    - temperature (np.ndarray): An array of temperature readings.
    - humidity (np.ndarray): An array of humidity readings.

    Returns:
    - np.ndarray: An array of calculated heat index values.
    """
    temp_square = temperature ** 2
    humid_square = humidity ** 2
    temp_humid = temperature * humidity

    return (C1 + C2 * temperature + C3 * humidity + C4 * temp_humid +
            C5 * temp_square + C6 * humid_square + C7 * temp_square * humidity +
            C8 * humid_square * temperature + C9 * temp_square * humid_square)