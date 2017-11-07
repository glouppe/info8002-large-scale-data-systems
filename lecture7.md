class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 7: Cloud computing

---

# Today

.center[![](figures/lec7/google-datacenter.jpg)]

How do we program this thing?
- MapReduce
- Spark
- Computational graph systems

---

# Dealing with lots of data

- Example: $130$+ trillion web pages $\times$ $50\text{KB} = 6.5$ exabytes.
    - ~$6500000$ hard drives ($1\text{TB}$) just to store the web.
- Assuming a data transfer rate of $200\text{MB}/s$, it would require $1000$+ years for a single computer to read the web!
    - And even more to make any useful usage of this data.
- Solution: **spread** the work over *many* machines.

---

# Traditional network programming

- Message-passing between nodes (MPI, RPC, etc).
- **Really hard** to do at scale (for 1000s of nodes):
    - How to *split* problem across nodes?
        - Important to consider network and data locality.
    - How to deal with *failures*?
        - a 10000-node clusters sees 10 faults/day.
    - Even without failure: *stragglers*.
        - Some nodes might be much slower than others.

---


# Traditional network programming

.center[![](figures/lec7/trends.png)]

.center[Almost nobody does message-passing anymore!$^*$]

.footnote[\*: except in niches, like scientific computing.]

---

# Data-Parallel models

- **Restrict** and **simplify** the programming interface so that the system can *do more automatically*.
- "Here is an operation, run it on all of the data".
    - I do not care *where* it runs (you schedule that).
    - In fact, feel free to run it *twice* on different nodes if needed.

---

# History

.center.width-100[![](figures/lec7/history.png)]

---

class: middle, center

# MapReduce

---

# What is MapReduce?

- **MapReduce** is a *parallel programming* model for processing distributed data on a cluster.
- Simple *high-level* API limited two operations: **Map** and **Reduce**, as inspired by Lisp primitives:
    - `map`: apply function to each value in a set.
        - `(map 'length '(() (a) (a b) (a b c)))` $\rightarrow$ `(0 1 2 3)`
    - `reduce`: combines all the values using a binary function.
        - `(reduce #'+ '(1 2 3 4 5))` $\rightarrow$ `15`
- MapReduce is best suited for *embarrassingly parallel* tasks.
    - When processing can be broken into parts of equal size.
    - When processes can concurrently work on these parts.
- Programmers do not have to worry about handling
    - parallelization
    - data distribution
    - load balancing
    - fault tolerance

---

# Programming model

- **Map**: input key/value pairs $\rightarrow$ intermediate key/value pairs
    - User function gets called for each input key/value pairs.
    - Produces a set of intermediate key/value pairs.
- **Reduce**: intermediate key/value pairs $\rightarrow$  result files
    - Combine all intermediate values for a particular key through a user-defined function.
    - Produces a set of merged output values.

---

# What really happens

- **Map worker**:
    - Map:
        - Map calls are distributed across machines by automatically partitioning the input data into $M$ *shards*.
        - Parse the input shards into input key/value pairs.
        - Process the input pairs through a user-defined `map` function to produce a set of intermediate key/value pairs.
        - Write the result to an intermediate file.
    - Partition:
        - Assign the result to one of $R$ reduce workers based on a partitioning function.
            - Both $R$ and the partitioning function are user defined.
- **Reduce worker**:
    - Sort:
        - Fetch the relevant partition of the output from all mappers.
        - Sort by keys.
            - Different mappers may have output the same key.
    - Reduce:
        - Accept an intermediate key and a set of values for the key.
        - For each unique, combine these values through a user-defined `reduce` function to form a smaller set of values.

---

# Overview

.center.width-100[![](figures/lec7/mr-full.png)]

---

# Step 1: Split input files

.center.width-100[![](figures/lec7/mr-shards.png)]

- Break up the input data into $M$ shards (typically $64 \text{MB}$).

---

# Step 2: Fork processes

.center.width-80[![](figures/lec7/mr-forks.png)]

- Start up many copies of the program on a cluster of machines.
    - 1 master: scheduler and coordinator
    - Lots of workers
- Idle workers are assigned either:
    - *map tasks*
        - each works on a shard
        - there are $M$ map tasks
    - *reduce tasks*
        - each works on intermediate files
        - there are $R$ reduce tasks

---

# Step 3: Map task

.center.width-50[![](figures/lec7/mr-read.png)]

- Read content of the input shard assigned to it.
- Parse key/value pairs $(k,v)$ out of the input data.
- Pass each pair to a **user-defined** `map` function.
    - Produce (one or more) intermediate key/value pairs $(k',v')$.
    - These are buffered in memory.

---

# Step 4: Create intermediate files

.center.width-70[![](figures/lec7/mr-if.png)]

- Intermediate key/value pairs $(k',v')$ produced by the user's `map` function are periodically written to *local* disk.
    - These files are partitioned into $R$ regions by a partitioning function, one for each reduce worker.
    - e.g., `hash(key) mod R`
- Notify master when complete.
    - Pass locations of intermediate data to the master.
    - Master forwards these locations to the reduce workers.

<span class="Q">[Q]</span> What is the purpose of the partitioning function?

---

# Step 5: Sorting/Shuffling

.center.width-60[![](figures/lec7/mr-reduce1.png)]

- Reduce worker get notified by master about the location of the intermediate files
associated to their partition.
- RPC to read the data from the local disks for the map workers.
- When the reduce worker reads intermediate data for its partition:
    - it sorts the data by intermediate keys $k'$.
    - all occurrences $v_i'$ of the same key are grouped together.

---

# Step 6: Reduce tasks

.center.width-60[![](figures/lec7/mr-reduce2.png)]

- The sorting phase grouped data with a unique intermediate key.
- The **user-defined** `reduce` function is given the key and the set of intermediate values for that key.
    - $(k', (v_1', v_2', v_3', ...))$
- The output of the `reduce` function is appended to an output file.

---

# Step 7: Return to user

- When all Map and Reduce tasks have completed, the master wakes up the user program.
- The MapReduce call in the user program returns and the program can resume execution.
    - The output of the operation is available in $R$ output files.

---

# Example: Counting words

.center.width-100[![](figures/lec7/mr-example.png)]

---

# Other examples

- *Distributed grep*
    - Search for words in lots of documents.
    - Map: emit a line if it matches a given pattern. Produce $(file,line)$ pairs.
    - Reduce: copy the intermediate data to the output.
- *Count URL access frequency*
    - Find the frequency of each URL in web logs.
    - Map: process logs of web page access. Produce $(url,1)$ pairs.
    - Reduce: add all values for the same URL.
- *Reverse web-link graph*
    - Find where page links come from.
    - Map: output $(target,source)$ pairs for each link $target$ in a web page $source$.
    - Reduce: concatenate the list of all source URLs associated with a target.

---

# MapReduce is widely applicable

.center[![](figures/lec7/mr-programs.png)]
.caption[Number of MapReduce programs in Google code source tree.]

---

# Fault tolerance

- Master *pings* each worker periodically.
    - If no response is received within a certain delay, the worker is marked as **failed**.
    - Map or Reduce tasks given to this worker are reset back to the initial state and rescheduled for other workers.
    - Task completion is committed through master to keep track of history.

<span class="Q">[Q]</span> What abstraction does this use?

<span class="Q">[Q]</span> What if the master node fails?

---

# Redundant execution

- Slow workers significantly lengthen completion time
    - Other jobs consuming resources on machine
    - Bad disks with soft errors transfer data very slowly
    - Weird things: processor caches disabled (!!)
- Solution: Near end of phase, spawn backup copies of tasks
    - Whichever one finishes first "wins"
- Effect: Dramatically shortens job completion time

---

# Locality

- Input and output files are stored on a distributed file system.
    - e.g., GFS or HDFS.
- Master tries to schedule Map workers near the data they are assigned to.
    - e.g., on the same machine or in the same rack.
- This results in thousands of machines reading input at local disk speed.
    - Without this, rack switches limit read rate.

---

.center.width-100[![](figures/lec7/mr-paper.png)]
.caption[Google, 2004.]

---

# Hadoop Ecosystem (1)

.center.width-100[![](figures/lec7/hadoop-eco.png)]

---

# Hadoop Ecosystem (2)

- *Hadoop HDFS*: A distributed file system for reliably storing huge amounts of unstructured, semi-structured and structured data in the form of files.
- **Hadoop MapReduce**: A distributed algorithm framework for the parallel processing of large datasets on *HDFS* filesystem. It runs on Hadoop cluster but also supports other database formats like *Cassandra* and *HBase*.
- *Cassandra*: A key-value pair NoSQL database, with column family data representation and asynchronous masterless replication.
- *HBase*: A key-value pair NoSQL database, with column family data representation, with master-slave replication. It uses HDFS as underlying storage.
- *Zookeeper*:  A distributed coordination service for distributed applications. It is based on **Paxos algorithm** variant called Zab.

---

# Hadoop Ecosystem (3)

- *Pig*: Pig is a scripting interface over MapReduce for developers who prefer scripting interface over native Java MapReduce programming.
- *Hive*:  Hive is a SQL interface over MapReduce for developers and analysts who prefer SQL interface over native Java MapReduce programming.
- *Mahout*: A library of machine learning algorithms, implemented on top of MapReduce, for finding meaningful patterns in HDFS datasets.
- *Yarn*: A system to schedule applications and services on an HDFS cluster and manage the cluster resources like memory and CPU.
- *Flume*: A tool to collect, aggregate, reliably move and ingest large amounts of data into HDFS.
- *Spark*: An in-memory data processing engine that can run a DAG of operations. It provides libraries for Machine Learning, SQL interface and near real-time Stream Processing
- ... and many others!

---

class: middle, center

# Spark

---

# MapReduce programmability

- Most applications require multiple MR steps.
    - Google indexing pipeline: 21 steps
    - Analytics queries (e.g., count clicks and top-K): 2-5 steps
    - Iterative algorithms (e.g., PageRank): 10s of steps
- Multi-step jobs create **spaghetti** code
    - 21 MR steps $\rightarrow$ 21 mapper and reducer classes
    - Lots of boilerplate code per step

.center.width-70[![](figures/lec7/mr-chaining.png)]
.caption[Chaining MapReduce jobs.]

---

# Problems with MapReduce

- Over time, MapReduce use cases showed two major limitations:
    - not all algorithms are suited for MapReduce.
        - e.g., a **linear dataflow** is forced.
    - it is difficult to use for exploration and **interactive** programming.
    - there are significant performance bottlenecks in iterative algorithms that *reuse* intermediate results.
        - e.g., saving intermediate results to stable storage (HDFS) is **very costly**.
- That is, MapReduce does not compose so well for large applications.
- For this reason, dozens of high level frameworks and specialized systems were developed.
    - e.g., Pregel, Dremel, FI, Drill, GraphLab, Storm, Impala, etc.

---

# Spark

.center.width-40[![](figures/lec7/spark-logo.png)]

- Like Hadoop MapReduce, **Spark** is a framework for performing distributed computations.
- Unlike various earlier specialized systems, the goal of Spark is to *generalize* MapReduce.
- Two small additions are enough to achieve that goal:
    - **fast data sharing**
    - general **direct acyclic graphs** (DAGs).
- Designed for data reuse and interactive programming.

---

# Programmability

.center.width-100[![](figures/lec7/spark-short.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Performance

Time to sort $100\text{TB}$:

.center.width-80[![](figures/lec7/spark-sort.png)]

.footnote[Credits: [sortbenchmark.org](http://sortbenchmark.org/)]

---

# RDD

- Programs in Spark are written in terms of a **Resilient Distributed Dataset** (RDD) abstraction and operations on them.
- An RDD is a **fault-tolerant** *read-only*, partitioned collection of records.
    - Resilient: built for fault-tolerance (it can be recreated).
    - Distributed: stored *in memory* across multiple nodes.
    - Dataset: collection of partitioned data with primitive values or values of values.
- RDDs can only be created through deterministic operations on either:
    - data in stable storage, or
    - other RDDs.

---

# Operations on RDDs

- *Transformations*: $f(\text{RDD}) \rightarrow \text{RDD'}$
    - Coarse-grained operations only.
        - It is not possible to write to a single specific location in an RDD.
    - Lazy evaluation (not computed immediately).
    - e.g., `map` or `filter`.
- *Actions*: $f(\text{RDD}) \rightarrow v$
    - Triggers computation.
    - e.g., `count`.
- The interface also offers explicit *persistence* mechanisms to indicate that an RDD will be reused in future operations.
    - This allows for internal optimizations.

---

# Workflow

.center.width-100[![](figures/lec7/spark-operations.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (1)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex1.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (2)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex2.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (3)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex3.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (4)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex4.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (5)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex5.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (6)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex6.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (7)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex7.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (8)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex8.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Example: Log mining (9)

Goal: Load error messages in memory, then interactively search for various patterns.

.center.width-100[![](figures/lec7/spark-ex9.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

# Rich, high-level API

.grid.center[
.col-1-3[
`map`<br>
`filter`<br>
`sort`<br>
`groupBy`<br>
`union`<br>
`join`<br>
...
]
.col-1-3[
`reduce`<br>
`count`<br>
`fold`<br>
`reduceByKey`<br>
`groupByKey`<br>
`cogroup`<br>
`zip`<br>
...
]
.col-1-3[
`sample`<br>
`take`<br>
`first`<br>
`partitionBy`<br>
`mapWith`<br>
`pipe`<br>
`save`<br>
...
]
]

---

# Lineage

- RDDs need not be materialized at all times.
- Instead, an RDD internally stores *how it was derived* from other datasets (its **lineage**) to compute its partitions from data in stable storage.
    - This derivation is expressed as coarse-grained transformations.
- Therefore, a program cannot reference an RDD that it cannot reconstruct after a failure.

.center.width-50[![](figures/lec7/lineage.png)]

---

# Representing RDDs

- RDDs are built around a **graph-based** representation (a DAG).
- RDDs share a common interface:
    - Lineage information:
        - Set of *partitions*.
        - List of *dependencies* on parents RDDs.
        - Function to *compute* a partition (as an iterator) given its parents.
    - Optimized execution (optional):
        - *Preferred locations* for each partition.
        - Partitioner (hash, range)

---

class: smaller

# Dependencies

.center.width-60[![](figures/lec7/spark-deps.png)]

- *Narrow dependencies*: each partition of the parent RDD is used by at most one partition of the child RDD.
    - Allow for pipelined execution on one node.
    - Recovery after failure is more efficient with a narrow dependency, as only the lost parents partitions need to be recomputed.
- *Wide dependencies*: multiple child partitions may depend on a parent partition.
    - A child partition requires data from all its parents to be recomputed.
---

# Execution process

.center.width-100[![](figures/lec7/spark-execution-process.png)]

.footnote[Credits: Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.]

---

class: smaller

# Job scheduler

.center.width-40[![](figures/lec7/spark-stages.png)]

- Whenever an *action* is called, the scheduler examines that RDD's lineage graph to build a **DAG of stages** to execute.
- Each *stage* contains as many pipeline transformations with narrow dependencies as possible.
- The boundaries of the stages are
    - the shuffle operations required for wide dependencies, or
    - already computed partitions that can short-circuit the computation of a parent RDD.
- The scheduler launches *tasks* to a lower-level scheduler to compute missing partitions from each stage until it has computed the target RDD.
- Tasks are assigned to machines based on *data locality*.

---

# Fault tolerance

- If a task fails, it is rescheduled on another node, as long as its stage's parents are still available.
- If some stages have become unavailable, all corresponding tasks are resubmit to compute the missing partitions in parallel.

.center.width-70[![](figures/lec7/spark-failure.png)]

---

# Dataflow programming

XXX

---

# Summary

xxx

---

# References

- Dean, Jeffrey, and Sanjay Ghemawat. "MapReduce: simplified data processing on large clusters." Communications of the ACM 51.1 (2008): 107-113.
- Zaharia, Matei, et al. "Resilient distributed datasets: A fault-tolerant abstraction for in-memory cluster computing." Proceedings of the 9th USENIX conference on Networked Systems Design and Implementation. USENIX Association, 2012.
- Xin, Reynold. "Stanford CS347 [Guest Lecture: Apache Spark](https://www.slideshare.net/rxin/stanford-cs347-guest-lecture-apache-spark)". 2015.
