import numpy as np
import unittest
from unittest.mock import patch
from src.app.app import calculate_heat_index_optimized, calculate_rolling_heat_index_optimized
from pandas import Timestamp


class TestCalculateRollingHeatIndexOptimized(unittest.TestCase):

    def test_calculate_heat_index_optimized(self):
        # Example input and expected output
        temperature = np.array([85, 90, 95])
        humidity = np.array([40, 50, 60])
        expected_output = np.array([84.32634,  94.59694, 113.09031])

        # Execute the function under test
        result = calculate_heat_index_optimized(temperature, humidity)

        # Verify the result
        np.testing.assert_array_almost_equal(result, expected_output,
                                             decimal=5,
                                             err_msg="Heat index calculation did not match expected output.")

    @patch('src.app.app.calculate_heat_index_optimized')
    def test_calculate_rolling_heat_index_optimized(self, mock_calculate_heat_index):
        # Setup mock return values that correspond to each input
        # Assuming the mock should return the sum of temperature and humidity as a simplified heat index for testing
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
