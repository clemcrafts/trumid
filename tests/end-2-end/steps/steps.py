import pandas as pd
import random
import numpy as np
import time

from behave import given, when, then
from deepdiff import DeepDiff
from src.app.app import calculate_rolling_heat_index_optimized
from src.app.baseline import calculate_rolling_heat_index


@given('we have generated a consistent set of test data')
def step_generate_test_data(context):
    """
    Generates a consistent set of test data with predefined cities and timestamps.
    This data is used for comparing the results of baseline and optimized methods
    for calculating the rolling heat index.
    """
    random.seed(0)
    np.random.seed(0)

    cities = ["New York", "Los Angeles", "Detroit", "Chicago", "San Francisco", "Seattle"]
    timestamps = pd.date_range("2024-02-01", "2024-02-05", freq="5h", tz="UTC")

    data = [
        {
            "city": city,
            "temperature": 20,
            "humidity": 30,
            "wind_speed": 40,  # Assuming wind_speed is used elsewhere or for completeness
            "reading_at": ts
        }
        for ts in timestamps for city in cities
    ]

    context.data = data

@when('we calculate the rolling heat index using the baseline method')
def step_calculate_baseline(context):
    """
    Calculates the rolling heat index for the test data using the baseline method.
    The results are stored in the context for later comparison.
    """
    context.results_baseline = calculate_rolling_heat_index(context.data)

@when('we calculate the rolling heat index using the optimized method')
def step_calculate_optimized(context):
    """
    Calculates the rolling heat index for the test data using the optimized method.
    This method is expected to produce the same results as the baseline but more efficiently.
    The results are stored in the context for later comparison.
    """
    context.results_optimized = calculate_rolling_heat_index_optimized(context.data)

@then('the results from both methods should be identical')
def step_compare_results(context):
    """
    Compares the results from the baseline and optimized methods using DeepDiff.
    Asserts that there are no differences, ensuring both methods are functionally equivalent.
    """
    diff = DeepDiff(context.results_baseline, context.results_optimized, ignore_order=True, significant_digits=3)
    assert diff == {}, f"Results differ: {diff}"

@when('we measure the execution time of the baseline method')
def step_measure_baseline_execution_time(context):
    """
    Measures the execution time of the baseline method for calculating the rolling heat index.
    The execution time is stored in the context for later comparison.
    """
    start_time = time.time()
    calculate_rolling_heat_index(context.data)
    context.baseline_execution_time = time.time() - start_time

@when('we measure the execution time of the optimized method')
def step_measure_optimized_execution_time(context):
    """
    Measures the execution time of the optimized method for calculating the rolling heat index.
    The execution time is stored in the context for later comparison with the baseline method's execution time.
    """
    start_time = time.time()
    calculate_rolling_heat_index_optimized(context.data)
    context.optimized_execution_time = time.time() - start_time

@then('the optimized method should be at least 90% faster than the baseline method')
def step_assess_optimization_efficiency(context):
    """
    Compares the execution time of the baseline and optimized methods, asserting that the optimized method
    is at least 90% faster than the baseline. This step ensures the optimization's efficiency goal is met.
    """
    improvement = 1 - (context.optimized_execution_time / context.baseline_execution_time)
    assert improvement >= 0.9, f"Optimization improvement was {improvement*100:.2f}%, expected at least 90%."