import time
from app import calculate_rolling_heat_index, store
from generate import generate_test_data
from datetime import datetime, timedelta
from config import BATCH_FREQUENCY_SECONDS


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
    # Initialize start and end dates
    start_date = datetime.strptime("2024-02-01", "%Y-%m-%d")
    end_date = datetime.strptime("2024-02-02", "%Y-%m-%d")

    while True:
        time.sleep(BATCH_FREQUENCY_SECONDS)

        # Convert dates to strings for the function call
        start_at_str = start_date.strftime("%Y-%m-%d")
        end_at_str = end_date.strftime("%Y-%m-%d")

        # Generate test data for the current date range
        result = calculate_rolling_heat_index(
            generate_test_data(start_at=start_at_str, end_at=end_at_str))

        # Store the result with the current timestamp
        store(datetime.now().time(), result)

        # Update the start and end dates for the next iteration
        start_date += timedelta(days=1)
        end_date += timedelta(days=1)


if __name__ == '__main__':
    run()