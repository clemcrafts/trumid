import numpy as np
import unittest
from unittest.mock import patch
from src.app.app import calculate_rolling_heat_index_optimized,calculate_heat_index  # Update with the actual module name


class TestCalculateRollingHeatIndexOptimized(unittest.TestCase):

    def test_calculate_heat_index(self):
        temperature = np.array([85, 90])
        humidity = np.array([70, 75])

        # Calculate the heat index using the provided constants
        expected_heat_index = calculate_heat_index(temperature, humidity)

        # Example expected values, replace with actual expected results based on the constants C1-C9
        actual_heat_index = np.array([92.70214919999987, 109.48049420000007])

        # Use np.testing.assert_array_almost_equal to compare arrays since floating point arithmetic can have small differences
        np.testing.assert_array_almost_equal(expected_heat_index, actual_heat_index, decimal=5)

    @patch('src.app.app.calculate_heat_index')
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
            {'city': 'CityA', 'temperature': 85, 'humidity': 70, 'heat_index': 155, 'rolling_heat_index': 155},
            {'city': 'CityA', 'temperature': 90, 'humidity': 75, 'heat_index': 165, 'rolling_heat_index': 160},
            {'city': 'CityB', 'temperature': 88, 'humidity': 65, 'heat_index': 153, 'rolling_heat_index': 153},
            {'city': 'CityB', 'temperature': 92, 'humidity': 60, 'heat_index': 152, 'rolling_heat_index': 152.5}
        ]


        # Call the function under test
        result = calculate_rolling_heat_index_optimized(readings)

        self.assertEqual(result, expected_output)
