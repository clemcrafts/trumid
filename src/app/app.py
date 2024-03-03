import pandas as pd
import numpy as np
import typing
from src.app.logger import logger
from src.app.config import (C1_HEAT_INDEX_COEFFICIENT,
                            C2_HEAT_INDEX_COEFFICIENT,
                            C3_HEAT_INDEX_COEFFICIENT,
                            C4_HEAT_INDEX_COEFFICIENT,
                            C5_HEAT_INDEX_COEFFICIENT,
                            C6_HEAT_INDEX_COEFFICIENT,
                            C7_HEAT_INDEX_COEFFICIENT,
                            C8_HEAT_INDEX_COEFFICIENT,
                            C9_HEAT_INDEX_COEFFICIENT)
from src.app.schema import ReadingsSchema
from marshmallow import ValidationError


def calculate_rolling_heat_index_optimized(
        readings: typing.List[dict],
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
    logger.info("Calculating rolling heat index...")
    df = pd.DataFrame(readings)

    try:
        df['reading_at'] = pd.to_datetime(df['reading_at'])
    except KeyError as error:
        logger.exception(
            f"The [reading_at] field is missing {error}: we discard the batch")
        return []
    df.set_index('reading_at', inplace=True)
    try:
        df['heat_index'] = calculate_heat_index_optimized(
            df['temperature'], df['humidity'])
    except KeyError as error:
        logger.exception(
            f"Heat-related field(s) are missing {error}: we discard the batch")
        return []
    try:
        df['rolling_heat_index'] = df.groupby('city')['heat_index'] \
            .transform(lambda x: x.rolling(rolling_freq, closed='both').mean())
    except TypeError as error:
        logger.exception(
            f"The rolling heat index failed because of a type issue: {error}."
            f"We discard the batch.")
        return []
    except Exception as error:
        logger.exception(
            f"The rolling heat index calculation failed: {error}. We discard the batch.")
        return []
    df.reset_index(inplace=True)
    return df.to_dict('records')


def calculate_heat_index_optimized(
        temperature: np.ndarray, humidity: np.ndarray) -> np.ndarray:
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
    return (C1_HEAT_INDEX_COEFFICIENT +
            C2_HEAT_INDEX_COEFFICIENT * temperature +
            C3_HEAT_INDEX_COEFFICIENT * humidity +
            C4_HEAT_INDEX_COEFFICIENT * temp_humid +
            C5_HEAT_INDEX_COEFFICIENT * temp_square +
            C6_HEAT_INDEX_COEFFICIENT * humid_square +
            C7_HEAT_INDEX_COEFFICIENT * temp_square * humidity +
            C8_HEAT_INDEX_COEFFICIENT * humid_square * temperature +
            C9_HEAT_INDEX_COEFFICIENT * temp_square * humid_square)


def validate_readings(readings):
    """
    Validate the payload before applying any logic.

    :param readings: List of dictionaries to validate.
    :return: List of validated dictionaries.
    """
    schema = ReadingsSchema(many=True)
    try:
        schema.load(readings)
    except ValidationError as err:
        logger.error(
            f"Validation errors, we're discarding the data: {err.messages}")
        return []
    return readings
