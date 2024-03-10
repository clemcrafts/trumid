# Trumid Take Home Task

There are 4 parts: (I) for the system assessment task (II) for the system improvement task (III) for the code optimization task and (IV) for the additional features.

## I. System Assessment Task

An assessment of a legacy architecture for the weather forecasting platform.

## a. Introduction
 
After analysis of the legacy architecture, I found major weak points and a couple of strong points:

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

### 3. The Event Processor is a Vulnerability and a Bottleneck
The event processor, tasked with managing an excessive number of input streams, emerges as another single point of failure. This overburdening raises concerns about the system's ability to maintain reliable performance under strain.

The event processor's role as a central hub for numerous input streams introduces significant risk, making it a bottleneck that could undermine the system's robustness and agility. This configuration, by centralizing too much logic and responsibility, limits the potential for efficient data handling and real-time responsiveness. Adopting a more modular approach, where duties are distributed among specialized components, could substantially improve the system's ability to evolve and handle diverse workloads with greater resilience.
### 4. Latency and Inefficiency Induced by SQL Databases
Incorporating SQL databases within a streaming architecture inherently introduces latency. This design choice can significantly hinder the real-time processing capabilities essential for the platform's effectiveness and responsiveness.

To ensure scalability and performance for a database servicing 1000 API users, employing a combination of read replicas, database sharding, caching mechanisms, load balancing, and auto-scaling is essential. These strategies collectively enhance query performance, reduce load on the primary database, ensure high availability, and enable the system to adapt dynamically to varying demand levels, thus maintaining a high-quality user experience as usage grows.

No sign of such database optimizations in the architecture schema!

### 5. Complexity from Excessive Service Layers
The architecture's reliance on numerous artificial service layers not only adds unnecessary complexity but also predisposes the system to increased latency. Simplifying these layers could enhance performance and reduce the risk of bottlenecks.

By doing so, the system can achieve a leaner, more efficient operational model, thereby mitigating the potential for delays and improving data throughput. Also, the queuing system between each steps seems a bit too artificial.

### 6. Overdiversification of Technologies
The platform's strategy of employing a wide array of technologies, while indicative of versatility, suggests a lack of focus that could complicate maintenance and integration. Streamlining the technology stack may improve efficiency and cohesiveness across the system.
This overdiversification can lead to increased overhead in both training for technical staff and in the complexity of operations. A more unified and carefully selected technology stack would not only ease the management burden but also enhance the system’s overall reliability and scalability, making it more adaptable to future needs and simplifications.

## b. Strengths

### 1. The Application is Using the Docker technology

The application's deployment strategy involves the use of Docker, ensuring that it runs within a container instead of being directly installed on the servers. 

This is not ideal and come with some red flags (like using docker-compose in production) but is a first step towards better containerization and orchestration as the OS, the libraries and the services are encapsulated in a full controlled image.

### 2. Horizontal Scaling for Processors and Pre-Processors

The system employs horizontal scaling for both processors and pre-processors, indicating an architecture designed to manage an increasing workload by adding more processes to the mix. 

This setup allows for the efficient preparation of data and calculation of forecasts, marking the onset of horizontal scaling. By distributing tasks across multiple processes, the system can handle larger volumes of data more effectively, laying the groundwork for scalable growth.

### 3. The Application Uses a Highly Efficient Message Bus

The application utilizes Kafka as its message bus, an excellent selection for a real-time weather forecasting platform. Kafka's strengths in providing high throughput, fault tolerance, and significant scalability align well with the demands of processing and distributing real-time weather data efficiently. 
This technology choice underscores the platform's commitment to robust and reliable data handling capabilities.

### 4. Simplicity of Deployment and Maintenance
A single virtual machine model simplifies the operational aspect of the application. It avoids the complexities associated with synchronizing multiple services across different servers or clusters. 
This approach reduces the immediate overheads related to infrastructure management, network configuration, and services syncrhonization, which are inherent in distributed systems. 


## c. Conclusion: Legacy Architecture Evaluation

### Average latency: *3 minutes*/hour and growing linearly then exponentially

Kafka's processing is near-instantaneous, maximum 1 second on an hour of streaming. With SQL loaders adding roughly 5 seconds (common query times against Postgres + redis), the event processor contributing about 5 seconds to merge data sources. 
Data preprocessors and processors taking 180 seconds (based on the baseline calculation of the coding task divided by 3 processors), data enrichers adding another 5 seconds, and the data sink taking around 5 seconds to write 15k cities forecast data in bulk in SQL.
We add 20% of network latency and get around 3 minutes.

### Maximum Throughput: 10 to 20 Mb/second
Without detailed performance benchmarks, it's challenging to provide an accurate number, but it's clear that the single VM setup and potential inefficiencies in data processing and storage could limit the system's maximum throughput to a point where it might struggle with significantly increased load.
Assuming that each stage is optimized but acknowledging the limitations of processing power and database I/O in a typical virtual machine environment, a realistic maximum throughput for this architecture could be around 10 to 20 MB/s.

### Cloud Costs per Year: $5000

For a VM equipped with 8 vCPUs and 32 GB RAM, you'd typically see expenses between $2,000 and $3,000. Adding to this, 1 TB of SSD storage for Redis would cost around $100 to $200. Networking might also add $100 to $300 to the bill. Then, factoring in scalable PostgreSQL storage, essential for managing the forecast data and historical records, could push the total upwards by an additional $1,000 to $2,000. Altogether, this integrated approach suggests an annual expenditure ranging from $3,200 to $5,500, underscoring the critical balance between system capability and cost management.


| Metric               | Expectation                                                                                                                               |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **Average Latency**  | 3 minutes/hour and growing exponentially                                                                                           |
| **Throughput**       | 10 to 20 Mb/second                                                                                                            |
| **Cloud Costs**      | $5000 for VM, additional costs for storage and networking                        |

## II. System Improvement Task

My new proposed architecture for the weather forecasting platform is as follows:

![Alt text](https://i.ibb.co/1mCkHPk/Screenshot-2024-03-10-at-13-50-14.png "Optional title")


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

### a. Exit virtual machine running docker-compose in production 

In the legacy architecture, if the forecasting service is down, Kafka is still running, the database is still ingesting inputs, the API is still serving results and the caching is still functional.

We suggest a service split allowing different scaling strategies and resilience in general:

![Alt text](https://i.ibb.co/RHkVg6K/Screenshot-2024-03-09-at-16-08-34.png "Services")

Here, if the forecasting service is down, Kafka is still running, the database is still ingesting inputs, the API is still serving results and the caching is still functional.

### b. Move from batching to streaming paradigm via Flink
Batching does not really scale because it forces you to consider batch of data in a suboptimal way when streaming technologies do that for you at a lower level under the hood.
Also, it seems like the application is not leveraging any distributed processing and Flink is great for that, mixing functional programming and distributed cumputations.

Here is a snippet of what could be done, keying by city, windowing for every minute:


```
// Define a Flink Streaming Execution Environment
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Configure source, e.g., from a Kafka topic
DataStream<String> input = env.addSource(new FlinkKafkaConsumer<>("weather_input_topic", new SimpleStringSchema(), properties));

// Parse the input stream to a WeatherData type
DataStream<WeatherData> parsedStream = input.map(value -> {
    return new ObjectMapper().readValue(value, WeatherData.class);
}).returns(WeatherData.class);

// Assign timestamps and watermarks
DataStream<WeatherData> timestampedStream = parsedStream
        .assignTimestampsAndWatermarks(new BoundedOutOfOrdernessTimestampExtractor<WeatherData>(Time.seconds(5)) {
            @Override
            public long extractTimestamp(WeatherData weatherData) {
                return weatherData.getTimestamp();
            }
        });

// Key by city and apply window
DataStream<WeatherData> windowedStream = timestampedStream
        .keyBy(WeatherData::getCity)
        .window(TumblingEventTimeWindows.of(Time.minutes(1)))
        .apply(new HeatIndexCalculation());

// Sink, e.g., to another Kafka topic or a database
windowedStream.addSink(new FlinkKafkaProducer<>("forecast_output_topic", new WeatherDataSchema(), properties));

// Execute the Flink job
env.execute("Heat Index Calculation Job");
```

I've contributed to build the entire realtime recommendation system with Flink for the TikTok-like video app Triller (https://triller.co/) and it was stunning in terms of performance. 

### c. Auto-scaling with Flink and Kubernetes
The use of Kubernetes is duplicating the number of Flink clusters, allows the forecasting service to auto-scale at 2 levels.
First, the flink job is scaling with load on different clusters.

![Alt text](https://i.ibb.co/XbmmC5c/Screenshot-2024-03-08-at-19-26-48.png "Flink Autoscaling")

With such a setup, Kubernetes will scale up the number of Flink clusters (with task managers) when if the load peaks and then scale it down when it drops.
 
An experiment is available on the Flink's blog, showing how an increase of lag on an input Kafka topic will generate an increase of resource consumption scaling up the number of task managers decreasing the load.

![Alt text](https://i.ibb.co/yyFxs6L/Screenshot-2024-03-08-at-19-40-27.png "Flink Autoscaling")

### d. Queues/Processors replaced by State-Based Distributed Processing

Replacing traditional queues and processors with state-based distributed processing, as facilitated by Flink's in-memory state management, marks a significant leap in performance efficiency. Flink's approach minimizes the need for data to traverse multiple, distinct processing layers, allowing for faster, more efficient computation. This model ensures data locality and reduces latency, as state is managed and processed closer to the data, eliminating bottlenecks associated with separate, non-distributed processors and improving overall system responsiveness.

![Alt text](https://i.ibb.co/9s1gzvm/Screenshot-2024-03-08-at-20-59-44.png "Flink States")

The S3 states can be plugged to a warehouse for querying or synchronized to various key-values technologies.

## 2. Performance Improvements

### a. Enhanced Low-Latency Processing with Apache Flink
Apache Flink stands out as a formidable stream processing framework, renowned for its ability to deliver high performance, ensure system availability, and support real-time application requirements. Its distributed nature and efficient processing capabilities significantly reduce latency, eliminating the need for high-latency intermediary layers and streamlining the data flow from ingestion to output.

How fast? Up to 400k messages/second.

 <img src="https://i.ibb.co/1z4rwZC/Screenshot-2024-03-09-at-16-32-10.png" width="400" alt="Latency" style="display: block; margin-left: auto; margin-right: auto;">

### b. Streamlined Data Synchronization with Connectors
Integrating directly with data sources through connectors, Flink ensures seamless and synchronized data ingestion. This approach not only enhances data flow efficiency but also supports real-time processing needs by minimizing delays in data availability and processing.

It's easy to create a Postgres sink based on a Kafka topic in concluent, see: https://docs.confluent.io/cloud/current/connectors/cc-postgresql-sink.html.

![Alt text](https://i.ibb.co/W59qQ3y/Screenshot-2024-03-09-at-17-03-38.png)

### c. Database Optimization via Sharding/Schemas and Read-only Replicas
Implementing sharding alongside read-only replicas for the database layer significantly boosts the system's performance and availability. Sharding distributes data across multiple databases to balance the load and improve response times, while read-only replicas allow for efficient query handling, especially for read-intensive operations.

For example, a good idea is to create a read-replica per region depending on where the customers of the application are to minimize latency for users.

The master read/write instance is used by the Kafka sink and the read replica(s) by the API when users are querying the data.

![Alt text](https://i.ibb.co/gyrBHXV/Screenshot-2024-03-09-at-17-12-24.png)

It's a way to optimize latency and throughput for data so write and read are handled by different DB instances.

### d. Scalable API with Horizontal Scaling and Caching
The API layer is designed for scalability, employing horizontal scaling to accommodate varying loads seamlessly. By adding more instances as demand increases, the system ensures consistent performance under different conditions. Additionally, strategic use of caching minimizes direct hits to the database for frequently requested data, further enhancing the API's responsiveness and reducing latency.

## 2. Reliability and data quality Improvements

### a. Disaster Recovery and Seamless Deployment Capabilities
The application incorporates a disaster recovery strategy, ensuring continuity of service and data integrity in the event of system failures. Coupled with methodologies for no-downtime deployments, this approach not only enhances system reliability but also maintains uninterrupted access for users, critical for real-time weather forecasting services.

### b. Comprehensive Testing via Lower Environments
The introduction of lower environments (such as Development, Testing, and Staging) facilitates thorough testing and validation processes before any production release. This structured approach allows for the identification and resolution of issues in a controlled manner, significantly reducing the risk of introducing bugs or performance issues to the live environment. As a result, the overall reliability of the application is greatly improved, ensuring that updates enhance rather than compromise the user experience.

### c. Robust Data Validation with Avro Schema and Dead Letter Queue Mechanism
Utilizing Avro schema for data validation introduces a high level of data quality assurance by enforcing data structure and type conformity. This mechanism ensures that only correctly formatted data flows through the processing pipeline, reducing errors and inconsistencies. Furthermore, the implementation of a dead letter queue captures and isolates problematic data for further analysis and correction, preventing minor issues from escalating into major disruptions.

<img src="https://i.ibb.co/Tbph6m1/Screenshot-2024-03-09-at-19-07-39.png" width="400" alt="Latency" style="display: block; margin-left: auto; margin-right: auto;">



Together, these measures significantly enhance the reliability and quality of data within the system, crucial for accurate weather forecasting.


## 3. Conclusion: New Architecture Evaluation


### Average latency: *3 seconds*/hour and stable over time
Over an hour of streaming, the latency would be the sum of the Kafka latency, the Flink latency and the network effects.
Because of Kafka and Flink being extremely low latency, we account for 1 second each and ads another second of network effect.

### Maximum Throughput: 350Mb/second with auto-scaling on
350k/messages per second assuming 1kb per message gives around 350Mb/second with is around 35x the legacy architecture.

### Cloud Costs per Year: $30000
The cloud costs need to account for using Amazon MSK for Kafka, Amazon EMR for Flink, Amazon EKS for the API, along with S3 and RDS for PostgreSQL across four environments (Dev, QAT, Pre-Prod, Prod), with only the last two connected to live data, involves a more detailed calculation. These services, particularly when scaled for production workloads and redundancy, can significantly increase operational costs.

Amazon MSK, EMR, EKS, S3, and RDS form a comprehensive cloud infrastructure for the project, with costs ranging from $0.20 per hour for a small Kafka cluster to $0.25 for a basic Flink setup, and an additional $0.10 per hour for EKS management. Storage and database services via S3 and RDS introduce variable costs based on usage, making efficient resource management crucial for controlling expenses.

Considering these factors, a rough annual cloud cost estimation for a setup with these AWS services across four environments might range between $20,000 and $40,000, leaning towards the higher end if prioritizing redundancy, performance, and data volume.

| Metric               | Expectation                                                                                                                               |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **Average Latency**  | 3 seconds/hour and stable                                                                                           |
| **Throughput**       | 350Mb/second                                                                                                            |
| **Cloud Costs**      | $30000 on AWS                       |


# III. Code Optimization Task

## 1. Introduction

For the code optimization task, we optimized the code, provided a proof that the new version is running faster, 
integrated the test in a CI/CD with various sizes of datasets and tests (unit, integration, load), added a schema 
validation, dockerized an application around it and prepared a placeholder for deployment in Github actions.

If you want to run it on your local...:

```
virtualenv env -p python3
pip install -r src/app/requirements.txt
```

To run the unit and integration tests:

```
pip install -r tests/requirements.txt
python -m pytest tests
```

To run the end-2-end tests:

```
behave tests/end2end
```

To run a constant batch of randomnized data as an app:

```
python -m src.app.run
```

To run the docker image instead:

```
docker build -f src/app/Dockerfile -t weather-app .
docker run -p 8000:80 weather-app
```

To run a quick comparison between the baseline and the optimize code:

```
pip install -r src/app/requirements.txt
pip install -r tests/requirements.txt
python tests/comparison.py
```

To deploy the application: actions > CI/CD Pipeline > Run workflow

![Alt text](https://i.ibb.co/1mJ7p78/Screenshot-2024-03-10-at-00-07-47.png)


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

### c. Avoid re-calculating Operations

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

## 3. Correctness Analysis 

As part of the end-2-end tests with Behave, we verify that the baseline provided (baseline.py) is matching 
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

## 3. Performance Analysis

As part of the end-2-end tests with Behave, we test the performance versus the baseline against 
3 different datasets and ensure that it's always at least 97% faster on every CI/CD run.


```
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
``` 

For a plug-and-play script to compare baseline and optimized version, I've added tests/comparison.py:

![Alt text](https://i.ibb.co/fXc2xK8/Figure-1.png "Optional title")

The datasets and the results are described below, the large dataset is 1 city with a data point every minute:

| Dataset Size | Start Date  | End Date    | Frequency  | Optimized Execution Time (s) | Baseline Execution Time (s) |
|--------------|-------------|-------------|------------|------------------------------|-----------------------------|
| Small        | 2024-02-01  | 2024-02-02  | 10 mins    | 0.0112949                    | 0.5317707                   |
| Medium       | 2024-02-01  | 2024-02-02  | 2 mins     | 0.0353853                    | 3.8580707                   |
| Large        | 2024-02-01  | 2024-02-02  | 1 min      | 0.0851476                    | 6.7501430                   |


Not only the vectorized version is faster on a given dataset but scales better as the dataset grows.
To go even faster on even larger datasets would require the use of Spark/Dask in the cloud hosted on AWS EMR (for example) leveraging managed clusters, optimized for distributed map-reduce frameworks. 

## 3. CI/CD and other goodies

I've embedded all the tests (unit, integration, end-2-end) in a CI/CD pipeline to enforce 
correctness and performance checks on every push:

![Alt text](https://i.ibb.co/7YTbcKz/Screenshot-2024-03-07-at-22-04-07.png "Optional title")

The last stage is a mocked deployment stage of the docker image (see dockerfile running the app on a constant 
stream of randomnized data):

```
  deploy-to-dev:
    needs: end-to-end-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Log in to Docker Hub
        run: echo "docker/login-action@v1"
      - name: Build and push Docker image
        run: echo "Replace with docker push to yourusername/yourrepositoryname:yourtag via docker/build-push-action@v2"
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