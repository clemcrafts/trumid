import time
from datetime import datetime, timedelta
from src.app.logger import logger
from src.app.app import calculate_rolling_heat_index_optimized, validate_readings
from src.app.generate import generate_test_data
from src.app.config import BATCH_FREQUENCY_SECONDS


def run():
    """
    Running the heat index calculation application.

    The function continuously generates test data for a set of cities,
    with each iteration adding one day
    to the start and end dates used for data generation. The generated test
    data is then processed to calculate
    the rolling heat index, and the results are stored along with the
    current timestamp.
    """
    start_date = datetime.strptime("2024-02-01", "%Y-%m-%d")
    end_date = datetime.strptime("2024-02-02", "%Y-%m-%d")

    while True:
        logger.info("New Batch...")
        time.sleep(BATCH_FREQUENCY_SECONDS)
        start_at_str = start_date.strftime("%Y-%m-%d")
        end_at_str = end_date.strftime("%Y-%m-%d")
        try:
            readings = generate_test_data(start_at=start_at_str, end_at=end_at_str)
        except Exception as error:
            logger.info(f"An error occurred when generating the data {error}")
            return
        try:
            valid_readings = validate_readings(readings)
        except Exception as error:
            logger.info(f"An error occurred when validating the data: {error}")
            continue
        try:
            calculate_rolling_heat_index_optimized(valid_readings)
        except Exception as error:
            logger.info(f"An error occurred when calculating the heat index: {error}")
            continue
        start_date += timedelta(days=1)
        end_date += timedelta(days=1)


if __name__ == "__main__":
    run()
