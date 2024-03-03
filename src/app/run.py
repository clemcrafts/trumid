import time
from app import calculate_rolling_heat_index, store
from generate import generate_test_data
from datetime import datetime
from config import BATCH_FREQUENCY_SECONDS


def run():
    """
    Running the data ingestion application.
    :return:
    """
    while True:
        time.sleep(BATCH_FREQUENCY_SECONDS)
        result = calculate_rolling_heat_index(generate_test_data())
        store(datetime.now().time(), result)

if __name__ == '__main__':
    run()