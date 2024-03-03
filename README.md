# Trumid Take Home Task

## I. System Assessment Task

Oh boy! This architecture looks complicated: it's never a good sign.
We want it simple. Here is a list of all the issues I found.

### 1. Running on one virtual machine is a single point of failure (SPOF). 
The fact that this is running on docker-compose in production is also a big red flag.

### 2. Data Reloading Efficiency: Reloading all data is not be efficient. 
Reloading all data from PostgreSQL into Redis every 5 minutes is not be efficient. 
This approach could lead to unnecessary processing and network load, especially as only a small fraction of the data changes frequently.

### 3. The event processor is a SPOF: it ingests too many input streams


### 4. SQL databases in the middle of a streaming design brings latency

### 5. Too many artificial sevices layers: complexity and latency incoming

### 6. Too many technologies at use 
It's not a contest of the maximum amount of technos! Each time you add a new techno to a stack without a very strong reason, you increase the complexity, maintenance cost when you could leverage one valid techno.