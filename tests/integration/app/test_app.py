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
            {'reading_at': Timestamp('2024-01-01 00:00:00'), 'city': 'CityA', 'temperature': 85, 'humidity': 70, 'heat_index': 92.70214919999987, 'rolling_heat_index': 92.70214919999987},
            {'reading_at': Timestamp('2024-01-01 12:00:00'), 'city': 'CityA', 'temperature': 90, 'humidity': 75, 'heat_index': 109.48049419999984, 'rolling_heat_index': 101.09132169999985},
            {'reading_at': Timestamp('2024-01-01 00:00:00'), 'city': 'CityB', 'temperature': 88, 'humidity': 65, 'heat_index': 97.56265522000008, 'rolling_heat_index': 97.56265522000008},
            {'reading_at': Timestamp('2024-01-01 12:00:00'), 'city': 'CityB', 'temperature': 92, 'humidity': 60, 'heat_index': 104.68441863999982, 'rolling_heat_index': 101.12353692999994}
        ]
        result = calculate_rolling_heat_index_optimized(readings)
        self.assertEqual(result, expected_output)
