import numpy as np
import unittest
from src.app.app import calculate_rolling_heat_index_optimized,calculate_heat_index  # Update with the actual module name


class TestCalculateRollingHeatIndexOptimized(unittest.TestCase):

    def test_calculate_rolling_heat_index_optimized(self):
        readings = [
            {"city": "CityA", "reading_at": "2024-01-01 00:00:00", "temperature": 85, "humidity": 70},
            {"city": "CityA", "reading_at": "2024-01-01 12:00:00", "temperature": 90, "humidity": 75},
            {"city": "CityB", "reading_at": "2024-01-01 00:00:00", "temperature": 88, "humidity": 65},
            {"city": "CityB", "reading_at": "2024-01-01 12:00:00", "temperature": 92, "humidity": 60}
        ]

        expected_output = [
            {'city': 'CityA', 'temperature': 85, 'humidity': 70, 'heat_index': 92.70214919999987, 'rolling_heat_index': 92.70214919999987},
            {'city': 'CityA', 'temperature': 90, 'humidity': 75, 'heat_index': 109.48049420000007, 'rolling_heat_index': 101.09132169999997},
            {'city': 'CityB', 'temperature': 88, 'humidity': 65, 'heat_index': 97.56265522000008, 'rolling_heat_index': 97.56265522000008},
            {'city': 'CityB', 'temperature': 92, 'humidity': 60, 'heat_index': 104.68441864000005, 'rolling_heat_index': 101.12353693000006}
        ]
        result = calculate_rolling_heat_index_optimized(readings)
        self.assertEqual(result, expected_output)
