import matplotlib.pyplot as plt
import timeit
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from src.app.generate import generate_test_data
from src.app.app import \
    calculate_rolling_heat_index_optimized  # Adjust import path as needed
from src.app.baseline import \
    calculate_rolling_heat_index  # Adjust import path as needed

# Define dataset sizes to test
dataset_sizes = ['small', 'medium', 'large', 'very large']
dataset_configurations = {
    'small': {'start_at': '2024-02-01', 'end_at': '2024-02-02', 'freq': '1H'},
    'medium': {'start_at': '2024-02-01', 'end_at': '2024-02-02',
               'freq': '30T'},
    'large': {'start_at': '2024-02-01', 'end_at': '2024-02-02', 'freq': '15T'},
    'very large': {'start_at': '2024-02-01', 'end_at': '2024-02-08', 'freq': '15T'}
}

# Store execution times
execution_times = {
    'optimized': [],
    'baseline': []
}

for size in dataset_sizes:
    config = dataset_configurations[size]
    config = dataset_configurations[size]
    print(f"Generating {size} dataset...")
    data = generate_test_data(config['start_at'], config['end_at'],
                              config['freq'])

    # Measure execution time for optimized function
    start_time = timeit.default_timer()
    calculate_rolling_heat_index_optimized(data)
    optimized_time = timeit.default_timer() - start_time
    execution_times['optimized'].append(optimized_time)

    # Measure execution time for baseline function
    start_time = timeit.default_timer()
    calculate_rolling_heat_index(data)
    baseline_time = timeit.default_timer() - start_time
    execution_times['baseline'].append(baseline_time)

# Plotting results
fig, ax = plt.subplots()
index = range(len(dataset_sizes))
bar_width = 0.35
opacity = 0.8

rects1 = ax.bar(index, execution_times['optimized'], bar_width,
                alpha=opacity, color='b', label='Optimized')

rects2 = ax.bar([p + bar_width for p in index], execution_times['baseline'],
                bar_width,
                alpha=opacity, color='r', label='Baseline')

ax.set_xlabel('Dataset Size')
ax.set_ylabel('Execution Time (seconds)')
ax.set_title('Heat Index Calculation Time by Method and Dataset Size')
ax.set_xticks([p + bar_width / 2 for p in index])
ax.set_xticklabels(dataset_sizes)
ax.legend()

plt.tight_layout()
plt.show()