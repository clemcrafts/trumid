from .config import C1, C2, C3, C4, C5, C6, C7, C8, C9
import pandas as pd
import numpy as np
import typing

def calculate_rolling_heat_index_optimized(readings: typing.List[dict],
                                           rolling_freq: str = "1D") -> typing.List[dict]:
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
    """Vectorized version of heat index calculation, optimized with pre-calculated squares."""
    temp_square = temperature ** 2
    humid_square = humidity ** 2
    temp_humid = temperature * humidity

    return (C1 + C2 * temperature + C3 * humidity + C4 * temp_humid +
            C5 * temp_square + C6 * humid_square + C7 * temp_square * humidity +
            C8 * humid_square * temperature + C9 * temp_square * humid_square)