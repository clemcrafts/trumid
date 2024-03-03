import time
from datetime import datetime, timedelta
from src.app.app import calculate_rolling_heat_index_optimized
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
        print("New Batch...")
        time.sleep(BATCH_FREQUENCY_SECONDS)

        # Convert dates to strings for the function call
        start_at_str = start_date.strftime("%Y-%m-%d")
        end_at_str = end_date.strftime("%Y-%m-%d")

        # Generate test data for the current date range
        calculate_rolling_heat_index_optimized(
            generate_test_data(start_at=start_at_str, end_at=end_at_str))

        # Update the start and end dates for the next iteration
        start_date += timedelta(days=1)
        end_date += timedelta(days=1)


if __name__ == '__main__':
    run()