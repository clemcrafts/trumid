from pandas import Timestamp
import unittest
from src.app.app import calculate_rolling_heat_index_optimized


class TestCalculateRollingHeatIndexOptimized(unittest.TestCase):
    """
    This test class is designed to validate the functionality of the
    calculate_rolling_heat_index_optimized function from the src.app.app module.
    It ensures that the function correctly calculates and returns the heat index and
    its rolling average based on temperature and humidity readings from different cities
    over specific timestamps.
    """

    def test_calculate_rolling_heat_index_optimized(self):
        """
        Tests whether the calculate_rolling_heat_index_optimized function accurately computes
        the heat index and its rolling average for a set of predefined temperature and humidity
        readings. This test verifies that the calculated values match the expected output,
        demonstrating the function's ability to handle input data correctly and produce
        consistent results.

        The test provides a list of readings, each containing city, timestamp, temperature,
        and humidity information. It checks if the function's output matches the expected
        heat index values and their rolling averages, ensuring accuracy in the calculation.
        """
        readings = [
            {"city": "CityA", "reading_at": "2024-01-01 00:00:00", "temperature": 85, "humidity": 70},
            {"city": "CityA", "reading_at": "2024-01-01 12:00:00", "temperature": 90, "humidity": 75},
            {"city": "CityB", "reading_at": "2024-01-01 00:00:00", "temperature": 88, "humidity": 65},
            {"city": "CityB", "reading_at": "2024-01-01 12:00:00", "temperature": 92, "humidity": 60}
        ]

        expected_output = [
            {'reading_at': Timestamp('2024-01-01 00:00:00'), 'city': 'CityA', 'temperature': 85.0, 'humidity': 70.0, 'heat_index': 92.70219421386719, 'rolling_heat_index': 92.70219421386719},
            {'reading_at': Timestamp('2024-01-01 12:00:00'), 'city': 'CityA', 'temperature': 90.0, 'humidity': 75.0, 'heat_index': 109.48046112060547, 'rolling_heat_index': 101.09132766723633},
            {'reading_at': Timestamp('2024-01-01 00:00:00'), 'city': 'CityB', 'temperature': 88.0, 'humidity': 65.0, 'heat_index': 97.56265258789062, 'rolling_heat_index': 97.56265258789062},
            {'reading_at': Timestamp('2024-01-01 12:00:00'), 'city': 'CityB', 'temperature': 92.0, 'humidity': 60.0, 'heat_index': 104.68445587158203, 'rolling_heat_index': 101.12355422973633}
        ]

        result = calculate_rolling_heat_index_optimized(readings)
        self.assertEqual(result, expected_output)
