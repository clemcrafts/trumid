# Trumid Take Home Task

## I. System Assessment Task

Oh boy! This architecture looks complicated: it's never a good sign.
We want it simple. Here is a list of all the issues I found:

![Alt text](https://i.ibb.co/WgmR2CT/Screenshot-2024-03-04-at-14-41-03.png "Optional title")

## a. Strengths

### 1. The application is leveraging Docker 
Even if not done the right way via docker-compose in production, the application is dockerized and it's a good thing.

### 2. Multiple containers share the (pre)-processing load
Multiple containers are handling the same work, this is a first step for potential horizontal auto-scaling.

### 3. The application is leveraging a distributed message bus 
The application is using Kafka which is distributed, fault-resistant and a good technology at scale.

## b. Weaknesses

### 1. Running on one virtual machine is a single point of failure (SPOF). 
The fact that this is running on docker-compose in production is also a big red flag.

### 2. Data Reloading Efficiency: Reloading all data is not be efficient. 
Reloading all data from PostgreSQL into Redis every 5 minutes is not be efficient. 
This approach could lead to unnecessary processing and network load, especially as only a small fraction of the data changes frequently.

### 3. The event processor is a SPOF: it ingests too many input streams


### 4. SQL databases in the middle of a streaming design brings latency

### 5. Too many artificial services layers: complexity and latency incoming

### 6. Too many technologies at use 
It's not a contest of the maximum amount of technos! Each time you add a new techno to a stack without a very strong reason, you increase the complexity, maintenance cost when you could leverage one valid techno.