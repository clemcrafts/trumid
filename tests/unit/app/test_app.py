import numpy as np
import unittest
from unittest.mock import patch
from src.app.app import calculate_heat_index_optimized, calculate_rolling_heat_index_optimized
from pandas import Timestamp


class TestCalculateRollingHeatIndexOptimized(unittest.TestCase):
    """
    A test suite for validating the calculate_rolling_heat_index_optimized and calculate_heat_index_optimized
    functions from the src.app.app module. It includes tests for accuracy of calculations and the functionality
    of the rolling heat index calculation with mocked dependencies.
    """

    def test_calculate_heat_index_optimized(self):
        """
        Tests the calculate_heat_index_optimized function for accuracy by comparing the calculated heat index
        values against expected results for a set of predefined temperature and humidity values.
        """
        temperature = np.array([85, 90, 95])
        humidity = np.array([40, 50, 60])
        expected_output = np.array([84.32634,  94.59694, 113.09031])

        result = calculate_heat_index_optimized(temperature, humidity)

        np.testing.assert_array_almost_equal(result, expected_output,
                                             decimal=5,
                                             err_msg="Heat index calculation did not match expected output.")

    @patch('src.app.app.calculate_heat_index_optimized')
    def test_calculate_rolling_heat_index_optimized(self, mock_calculate_heat_index):
        """
         Tests the calculate_rolling_heat_index_optimized function using a
         mocked version of
         calculate_heat_index_optimized to verify the rolling calculation
         and aggregation logic.
         Mocking allows for simplified testing of the rolling functionality
         independent of the
         actual heat index calculation logic.

         Parameters:
         - mock_calculate_heat_index: The mock object for the
         calculate_heat_index_optimized function,
           provided by the 'unittest.mock.patch' decorator.
         """
        mock_calculate_heat_index.side_effect = lambda temperature, humidity: temperature + humidity

        readings = [
            {"city": "CityA", "reading_at": "2024-01-01 00:00:00", "temperature": 85, "humidity": 70},
            {"city": "CityA", "reading_at": "2024-01-01 12:00:00", "temperature": 90, "humidity": 75},
            {"city": "CityB", "reading_at": "2024-01-01 00:00:00", "temperature": 88, "humidity": 65},
            {"city": "CityB", "reading_at": "2024-01-01 12:00:00", "temperature": 92, "humidity": 60}
        ]

        # Expected output assuming mocked heat index calculation as mentioned
        expected_output = [
          {'reading_at': Timestamp('2024-01-01 00:00:00'), 'city': 'CityA', 'temperature': 85.0, 'humidity': 70.0, 'heat_index': 155.0, 'rolling_heat_index': 155.0},
          {'reading_at': Timestamp('2024-01-01 12:00:00'), 'city': 'CityA', 'temperature': 90.0, 'humidity': 75.0, 'heat_index': 165.0, 'rolling_heat_index': 160.0},
          {'reading_at': Timestamp('2024-01-01 00:00:00'), 'city': 'CityB', 'temperature': 88.0, 'humidity': 65.0, 'heat_index': 153.0, 'rolling_heat_index': 153.0},
          {'reading_at': Timestamp('2024-01-01 12:00:00'), 'city': 'CityB', 'temperature': 92.0, 'humidity': 60.0, 'heat_index': 152.0, 'rolling_heat_index': 152.5}
        ]

        # Call the function under test
        result = calculate_rolling_heat_index_optimized(readings)
        self.assertEqual(result, expected_output)
