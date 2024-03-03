Feature: Compare optimized and baseline heat index calculations

  Scenario: Calculate rolling heat index using both methods and compare
    Given we have generated a small dataset
    When we calculate the rolling heat index using the baseline method
    And we calculate the rolling heat index using the optimized method
    Then the results from both methods should be identical

  Scenario: Assess optimization efficiency for a small dataset
    Given we have generated a small dataset
    When we measure the execution time of the baseline method
    And we measure the execution time of the optimized method
    Then the optimized method should be at least 97% faster than the baseline method

  Scenario: Assess optimization efficiency for a medium dataset
    Given we have generated a medium dataset
    When we measure the execution time of the baseline method
    And we measure the execution time of the optimized method
    Then the optimized method should be at least 97% faster than the baseline method

  Scenario: Assess optimization efficiency for a large dataset
    Given we have generated a large dataset
    When we measure the execution time of the baseline method
    And we measure the execution time of the optimized method
    Then the optimized method should be at least 97% faster than the baseline method
