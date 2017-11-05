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

- **Restrict** the programming interface so that the system can *do more automatically*.
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
- Simple *high-level* API limited two operations: **Map** and **Reduce**, as inspired by Lisp:
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

- **Map**: input shard $\rightarrow$ intermediate key/value pairs
    - Map calls are distributed across machines by automatically partitioning the input data into $M$ *shards*.
    - User function gets called for each shard of input.
    - The MapReduce framework groups together all intermediate values associated with the same intermediate key and passes them to the Reduce function.
- **Reduce**: intermediate key/value pairs $\rightarrow$  result files
    - Accepts an intermediate key and a set of values for the key.
    - Merges these values together to form a smaller set of values by calling a user function for each unique key.
    - Reduce calls are distributed by partitioning the intermediate key space into $R$ pieces.

---

# What really happens

- **Map worker**:
    - Map:
        - Parse the input data into key/value pairs.
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
        - Input is the sorted output of mappers.
        - To aggregate the results, call the user-defined reduce function for each key, along with the list of values for that key.

---

# The complete picture

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
- Parse key/value pairs out of the input data.
- Pass each pair to a user-defined `map` function.
    - Produce intermediate key/value pairs.
    - These are buffered in memory.

---

# Step 4: Create intermediate files

.center.width-70[![](figures/lec7/mr-if.png)]

- Intermediate key/value pairs produced by the user's `map` function are periodically written to *local* disk.
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
    - it sorts the data by intermediate keys.
    - all occurrences of the same key are grouped together.

---

# Step 6: Reduce tasks

.center.width-60[![](figures/lec7/mr-reduce2.png)]

- The sorting phase grouped data with a unique intermediate key.
- The user-defined `reduce` function is given the key and the set of intermediate values for that key.
    - `<key, (value1, value2, value3, ...)>`
- The output of the `reduce` function is appended to an output file.

---

# Step 7: Return to user

- When all Map and Reduce tasks have completed, the master wakes up the user program.
- The MapReduce call in the user program returns and the program can resume execution.
    - The output of the operation is available in $R$ output files.

---

# Example

XXX

---

# Fault tolerance

- Master *pings* each worker periodically.
    - If no response is received within a certain delay, the worker is marked as **failed**.
    - Map or Reduce tasks given to this worker are reset back to the initial state and rescheduled for other workers.

<span class="Q">[Q]</span> What abstraction does this use?

<span class="Q">[Q]</span> What if the master node fails?

---

# Locality

- Input and output files are stored on a distributed file system.
    - e.g., GFS or HDFS.
- Master tries to schedule Map workers near the data they are assigned to.
    - e.g., on the same machine or in the same rack.
- This results in less network communication and better performance.

---

# History of MapReduce

---

MR paper

---

# Hadoop Ecosystem

---

class: middle, center

# Spark

---

# Limitations of MapReduce

- MR programmability (slide 9)

---

# Spark

---

# RDD

---

class: middle, center

# Computational graph systems

---

# Summary

---

# References
