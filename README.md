# Trumid Take Home Task

## I. System Assessment Task

## a. Introduction
 


![Alt text](https://i.ibb.co/WgmR2CT/Screenshot-2024-03-04-at-14-41-03.png "Optional title")

## a. Weaknesses

### 1. Single Point of Failure in Hosting
Utilizing a single virtual machine for running the entire platform introduces a significant risk of downtime, as it serves as a single point of failure (SPOF). Employing docker-compose in a production setting further exacerbates this vulnerability, signaling a critical area for improvement.

Based on the description of the application, it also seems that there is no multi-environments setup (e.g: DEV/QAT/PROD) with a healthy development lifecycle allowing testing of the solution before deployment to production. There is also no iso-production environment for disaster recovery in case the application goes down.
### 2. Inefficient Data Reloading Practices
The strategy of reloading all data from PostgreSQL into Redis at five-minute intervals is highly inefficient. This process not only imposes unnecessary burdens on processing capabilities and network resources but also fails to address the reality that only a minor portion of the data requires frequent updates.

The data volume from 15,000 cities at 1-minute granularity, with one entry of the time series for one city being around 100 bytes, 
equates to approximately 0.024 MB/s (megabytes per second) which is 85.83 MB per hour and 2.06 GB. That's 734.28 GB after a year.

With a moderate network speed (1 Gbps), the read speeds might be closer to 100-150 MB/s, and network throughput would be about 125 MB/s. In this case, querying 700GB could take approximately 1.5 to 2 hours (!) which is not acceptable to simply update the cache and will lead to data freshness issue and decrease of performance.

### 3. Event Processor Vulnerability
The event processor, tasked with managing an excessive number of input streams, emerges as another single point of failure. This overburdening raises concerns about the system's ability to maintain reliable performance under strain.

### 4. Latency Induced by SQL Databases
Incorporating SQL databases within a streaming architecture inherently introduces latency. This design choice can significantly hinder the real-time processing capabilities essential for the platform's effectiveness and responsiveness.

To ensure scalability and performance for a database servicing 1000 API users, employing a combination of read replicas, database sharding, caching mechanisms, load balancing, and auto-scaling is essential. These strategies collectively enhance query performance, reduce load on the primary database, ensure high availability, and enable the system to adapt dynamically to varying demand levels, thus maintaining a high-quality user experience as usage grows.

No sign of such database optimizations in the architecture schema!

### 5. Complexity from Excessive Service Layers
The architecture's reliance on numerous artificial service layers not only adds unnecessary complexity but also predisposes the system to increased latency. Simplifying these layers could enhance performance and reduce the risk of bottlenecks.

### 6. Overdiversification of Technologies
The platform's strategy of employing a wide array of technologies, while indicative of versatility, suggests a lack of focus that could complicate maintenance and integration. Streamlining the technology stack may improve efficiency and cohesiveness across the system.



## b. Strengths

### 1. The Application is Leveraging Docker
The application capitalizes on Docker, encapsulating parts of the application for better control even as it currently operates primarily through docker-compose.
It potentially opens the door for more complex orchestration solutions as the application grows and its needs become more scalable.

### 2. Multiple containers share the processing and pre-processing load
Using multiple containers of the same service to distribute the (pre-)processing workload enhances efficiency but also lays 
the groundwork for potential horizontal auto-scaling later: auto-scaling would be ensuring that the platform can adjust to varying data demands.

### 3. The application is using a performant distributed message bus 
The application is using Kafka which is a very good choice for a real-time weather forecasting platform offering high throughput, fault tolerance and great scalability.

### 4. Simplicity of Deployment and Maintenance
A single virtual machine model simplifies the operational aspect of the application. It avoids the complexities associated with synchronizing multiple services across different servers or clusters. 
This approach reduces the immediate overheads related to infrastructure management, network configuration, and services syncrhonization, which are inherent in distributed systems. 


## c. Conclusion
Upon examining the system's architecture and operational strategies, 
it is clear that while there are occasional strengths, including Docker utilization, workload distribution there and there, and infrastructure simplicity, there are critical areas that necessitate improvement. 

The identified weaknesses, such as the single point of failure, inefficient data reloading practices, vulnerabilities in event processing, latency issues, excessive service layer complexity, and overdiversification of technologies, underline the need for a strategic overhaul. Addressing these challenges will not only mitigate risks but also enhance the system's overall scalability, performance, and reliability, thereby ensuring it can effectively meet current and future demands.

## II. System Improvement Task

![Alt text](https://i.ibb.co/0h01Ybv/Screenshot-2024-03-05-at-18-23-07.png "Optional title")


This involves a couple of microservices present on the architecture diagram (forecasting service, API service) and some others 
like a reporting service and a UI service. They auto-scale leveraging Kubernetes and the internal auto-scaling capabilities of Flink.


![Alt text](https://i.ibb.co/Qv3JTfy/Screenshot-2024-03-06-at-15-56-14.png "Optional title")

The CI/CD is running unit, integration and component test against each docker image. Eventually 2 load tests are performed using Locust.

The first one is a constant high load of messages (2x production load) and the second one is a fast ramp up in load intensity so simulate a bottleneck leading to a faster than usual acceleration of messages.


### 1. Scalability Improvements

The assumptions behind the scalability improvements is that the system might have to cope with higher frequency data in the future like a new data point per second for all 15k cities and bigger payloads increasing the need for high throughput.
In that case we want the system to be able to generate up to 15k/messages per second. 

The legacy system would be down in a couple of hours due to (1) exceeding VM RAM (2) exceeding acceptable latency having to retrieve Gb of data from the results table on every batch (3) simply killing the database with read/write load that a single instance with no replica won't be able to handle while serving data to users.

The new architecture provides the following benefits for scalability:

### a. Microservices split fixing the single point of failure 

First of all, scalability can be seen as a removal of the single point of failure.
Here, if the forecasting service is down, Kafka is still running, the database is still ingesting inputs, the API is still serving results and the caching is still functional.

### b. Move from batching to streaming paradigm
Batching does not really scale because it forces you to consider batch of data in a suboptimal way when streaming technologies do that for you at a lower level under the hood.


### c. Auto-scaling at multiple levels
The use of Kubernetes is duplicating the number of Flink clusters, allows the forecasting service to auto-scale at 2 levels.
First, the flink job is scaling with load on different clusters.

### d. The SQL database is not a bottleneck anymore
The SQL insertion and querying is not in the middle of the process anymore.

### 2. Performance Improvements

### a. Flink is a beast and removes high latency layers

Flink is a distributed low-level stream processing framework for high-performing, always-available, and realtime applications.

### b. The input topic is synchronized via a connector
Flink is a distributed low-level stream processing framework for high-performing, always-available, and realtime applications.



### c. The database is sharded with read-only replicas

### d. The API is scaling horizontally and leverages c aching

## 2. Reliability and data quality Improvements

### a. The Application has a disaster recovery mode and no-downtime deployment

### b. The lower environments allow advanced testing before a prod release

### c. Avro schema enables a robust data validation and a dead letter queue


## 3. Monitoring Improvement

### a. Microservices allows granular monitoring and alerting

It's now possible to monitor CPU, memory and latency by component (database, forecasting service, api, etc)

# III. Code Optimization Task

## 1. Introduction

For the code optimization task, we optimized the code, provided a proof that the new version is running faster, 
integrated the test in a CI/CD with various sizes of datasets and tests (unit, integration, load), added a schema 
validation, dockerized an application around it and prepared a placeholder for deployment in Github actions.

## 2. Code optimization

### a. Vectorize calculations with pandas

Pandas vectorization leverages highly optimized C and Cython operations under the hood, making data manipulation and mathematical operations 
much faster and more efficient than iterating through rows with loops.

This vectorized heat index calculation is order of magnitude faster than looping with apply:

```
calculate_heat_index_optimized(
    temperature: np.ndarray, humidity: np.ndarray
)
```

### b. Leverage groupby, transform, mean 

Pandas' built-in functions for group-wise operations and rolling calculationsare 
significantly faster and more efficient due to the use of optimized C and Cython operations, minimizing 
the overhead associated with Python loops.

```
df["rolling_heat_index"] = df.groupby("city")["heat_index"].transform(
            lambda x: x.rolling(rolling_freq, closed="both").mean()
```

### c. Avoid re-calculating operations

```
temp_square = temperature**2
humid_square = humidity**2
temp_humid = temperature * humidity
return (
        C1_HEAT_INDEX_COEFFICIENT
        + C2_HEAT_INDEX_COEFFICIENT * temperature
        + C3_HEAT_INDEX_COEFFICIENT * humidity
        + C4_HEAT_INDEX_COEFFICIENT * temp_humid
        + C5_HEAT_INDEX_COEFFICIENT * temp_square
        + C6_HEAT_INDEX_COEFFICIENT * humid_square
        + C7_HEAT_INDEX_COEFFICIENT * temp_square * humidity
        + C8_HEAT_INDEX_COEFFICIENT * humid_square * temperature
        + C9_HEAT_INDEX_COEFFICIENT * temp_square * humid_square
    )
```

## 3. Correctness analysis 

As part of the end-2-end tests with behave, we verify that the baseline provided (baseline.py) is matching 
the algorithm from our new app (app.py):

```
Scenario: Calculate rolling heat index using both methods and compare
 Given we have generated a small dataset
 When we calculate the rolling heat index using the baseline method
 And we calculate the rolling heat index using the optimized method
 Then the results from both methods should be identical
```

under the hood, it's a deep diff on the result with some reasonable tolerance:

```
@then("the results from both methods should be identical")
def step_compare_results(context):
    """
    Compares the results from the baseline and optimized methods using DeepDiff.
    Asserts that there are no differences, ensuring both methods are functionally equivalent.
    """
    diff = DeepDiff(
        context.results_baseline,
        context.results_optimized,
        ignore_order=True,
        ignore_numeric_type_changes=True,
        significant_digits=0,
    )
    assert diff == {}, f"Results differ: {diff}"
```

# IV. System Optional Task

## 1. BI Reporting Dashboard With Airflow and Tableau

With view delivered by Airflow:

![Alt text](https://i.ibb.co/9gtZ7Fm/Screenshot-2024-03-07-at-13-55-48.png "Optional title")

## 2. Advanced system monitoring via Prometheus

To monitor resources and system-level metrics, Prometheus and Grafana are the elephants in the room:

![Alt text](https://i.ibb.co/G9Q382S/Screenshot-2024-03-07-at-14-29-20.png "Optional title")

Giving a dashboard of resource and monitoring like:

![Alt text](https://i.ibb.co/k49pHby/Screenshot-2024-03-07-at-14-33-11.png "Optional title")

## 3. Logs Management and Centralization with Datadog

To monitor logs and errors across the entire stack, Datadog is a very popular solution giving a centralized 
view of your entire system with payloads, errors, messages tracking across services and much more:

![Alt text](https://i.ibb.co/9wTYCPm/Screenshot-2024-03-07-at-15-17-05.png "Optional title")

Giving log views that you can query, tagged by service, also giving a sense of the volume of messages processed:

![Alt text](https://i.ibb.co/gMJ3XKR/Screenshot-2024-03-07-at-15-07-49.png "Optional title")