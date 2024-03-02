Feature: Compare optimized and baseline heat index calculations

  Scenario: Calculate rolling heat index using both methods and compare
    Given we have generated a consistent set of test data
    When we calculate the rolling heat index using the baseline method
    And we calculate the rolling heat index using the optimized method
    Then the results from both methods should be identical

  Scenario: Measure execution time and assess optimization efficiency
    Given we have generated a consistent set of test data
    When we measure the execution time of the baseline method
    And we measure the execution time of the optimized method
    Then the optimized method should be at least 90% faster than the baseline method