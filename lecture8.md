class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 8: Distributed file systems

---

# Today

- *Google File System* (GFS)
    - Design considerations behind GFS .
    - Data replication
    - Reading and writing.
    - Recovery from failure
- *Hadoop Distributed File System* (HDFS)

.center.width-80[![](figures/lec8/hadoop-hdfs.png)]

---

class: middle, center

# Google File System

---

# File systems

- File systems determine **how** data is stored and retrieved.
- *Distributed file systems* manage the storage across a network of machines.
    - Single-system **illusion** for users.
    - Added complexity due to the network.
- GFS and HDFS are examples of distributed file systems.
    - They represent *one* way (not the way) to design a distributed file system.


<br><br><br><br><br><br><br><br><span class="Q">[Q]</span> Which file systems do you know?

---

# History

- GFS was developed at Google around 2003, jointly with MapReduce.
- Provide **efficient** and **reliable** access to data.
- Use large clusters of *commodity hardware*.
- Proprietary.

.center.width-80[![](figures/lec8/gfs-paper.png)]

---

# Assumptions

- Hardware **failures are common** (commodity hardware).
- Files are *large* (multi-GB files are the norm) and their number is (relatively) limited (millions).
- Reads:
    - *large streaming reads* ($\geq$ 1MB in size)
    - *small random reads*
- Writes:
    - Large **sequential writes** that *append* to files.
    - Concurrent appends by multiple clients.
    - Once written, files are *seldom modified* ($\neq$ append) again.
        - Random modification in files is possible, but not efficient in GFS.
- High sustained bandwidth, but low latency.

---

# Which of those fit the assumptions?

- Global company dealing with the data of its 100M employees.
    - Salary, bonuses, age, performance, etc.
- A search engine's query log.
- A hospital's medical imaging data generated from an MRI scan.
- Data sent by the Hubble telescope.
- A search engine's index (used to serve search results to users).

---

# How would you design a DFS?

.grid[
.col-1-2[
- We want *single system illusion* for data storage.
- Although data is too large be stored in a single system.
- Hardware **will** fail.

![](figures/lec8/google-first-server_a.jpg)
.caption[Google first servers]
]
.col-1-2[
![](figures/lec8/google-first-server.jpg)
]
]

---

# Disclaimer

- GFS (and HDFS) are **not a good fit** for:
    - Low latency data access (in the ms range).
        - Solution: distributed databases, such as HBase.
    - Many small files.
    - Constantly changing data.
- Not all details of GFS are public knowledge.

---

# Design aims

- Maintain data and system availability.
- Handle failures gracefully and transparently.
- Low synchronization overhead between entities.
- Exploit parallelism of numerous entities.
- Ensure high sustained throughput over low latency for individual reads/writes.

---

# Architecture

.center.width-100[![](figures/lec8/gfs-architecture.png)]

- A *single* **master** node.
- Many *chunkservers* (100s - 1000s) storing the data.
    - Physically spread in different racks.
- Many clients.

???

- Remember: one way, not the way.
- Data does not flow across the GFS master.

---

# Files

- A single **file** may contain several *objects*.
    - E.g., images, web pages, etc.
- Files are divided into fixed-size **chunks**.
    - Each chunk is identified by a globally unique 64 bit *chunk handle*.
- Chunkservers store chunks on local disks as plain Linux files.
    - Read or write data specified by a pair (chunk handle, byte range).
    - By default **three replicas** of a chunk stored across chunkservers.

.center.width-50[![](figures/lec8/gfs-chunks.png)]

---

# Master

- The master node stores and maintains *all file system metadata*:
    - Three main types of metadata:
        - the file and chunk namespaces,
        - the mapping from files to chunks,
        - the locations of each chunk's replicas.
    - All metadata is kept in master's **memory** (fast random access).
        - Sets limits on the entire system's capacity.
- It controls and coordinates *system-wide activities*:
    - Chunk lease management
    - Garbage collection of orphaned chunks
    - Chunk migration between chunkservers
- **Heartbeat** messages between master and chunkservers.
    - To detect failures
    - To send instructions and collect state information
- An *operation log* persists master's state to permanent storage.
    - In case master crashes, its state can be recovered (more later).

---

# One node to rule them  all

- Having a **single master** node vastly simplifies the system design.
- Enable master to make sophisticated chunk placement and replication decisions, using *global knowledge*.
- Its involvement in reads and writes should be minimized so to avoid that it becomes a bottleneck.
    - Clients never read and write file data through master.
    - Instead, clients ask the master which chunkservers it should contact.

<br><br><br><br><br><br><br><br><span class="Q">[Q]</span> As the cluster grows, can the master become a bottleneck?

???

Size of storage increased in the range of petabytes. The amount of metadata maintained by master increased and scanning through such large amounts became an issue. The single master started becoming a bottleneck when thousand client requests came simultaneously.

---

# Chunks

- Default size = 64MB.
    - This a **key design parameter** in GFS!
- Advantages of large (but not too large) chunk size:
    - **Reduced** need for client/master interaction.
    - 1 request per chunk suits the target workloads.
    - Client can cache *all the locations* for a multi-TB working set.
    - **Reduced size** of metadata on master (kept in memory).
- Disadvantage:
    - A chunkserver can become a **hotspot** for popular files.

<br><br><br><br><br><br><span class="Q">[Q]</span> How to fix the hotspot problem?

---

# <strike>Caching</strike>

- Clients do **not** cache file data.
    - They do cache metadata.
- Chunckservers do **not** cache file data.
    - Responsibility of the underlying file system (e.g., Linux's buffer cache).
- Client caches offer *little benefit* because most applications
    - stream through huge files
        - disk seek time negligible compared to transfer time.
    - have working sets too large to be cached.
- Not having a caching system **simplifies the overall system** by eliminating cache coherence issues.

---

# Interface

- No file system interface at the operating-system level (e.g., under the VFS layer).
    - User-level API is provided instead.
    - Does not support all the features of POSIX file system access.
        - But looks similar (i.e., `open`, `close`, `read`, `write`, ...)
- Two special operations are supported:
    - *Snapshot*: efficient way of creating a copy of the current instance of a file or directory tree.
    - *Append*: append data to a file as an **atomic operation**, without having to lock the file.
        - Multiple processes can append to the same file concurrently without overwriting one another's data.

---

# Reads (1)

.center.width-100[![](figures/lec8/gfs-read1.png)]

1) The GFS client translates filename and byte offset specified by the application into a *chunk index* within the file. A request is sent to master.

---

# Reads (2)

.center.width-100[![](figures/lec8/gfs-read2.png)]

2) Master replies with chunk handle and locations of the replicas.

---

# Reads (3+4)

.center.width-100[![](figures/lec8/gfs-read3.png)]

3) The client caches this information using the file name and chunk index as the key.
- Further reads of the same chunk requires no more client-master interaction, until the cached information expires.

4) The client sends a request to one of the replicas, typically the closest.

---

# Reads (5)

.center.width-100[![](figures/lec8/gfs-read4.png)]

5) The contacted chunkserver replies with the data.

---

# Leases and mutation order

- A **mutation** is an operation that changes the contents or metadata of a chunk.
    - `write`
    - `append`
- Each mutation is performed at all the chunk's replicas.
- **Leases** are used to maintain a consistent mutation order across replicas.
    - Master grants a chunk lease to one of the replicas, called the *primary*.
    - Leases are renewed using the periodic heartbeat messages between master and chunkservers.
- The primary picks a serial order for all mutations to the chunk.
    - All replicas follow this order when applying mutations.
- Leases and serial order at the primary define a *global ordering* of the operations on a chunk.


---

# Writes (1+2)

.center.width-40[![](figures/lec8/gfs-write12.png)]

1) The GFS client asks master for the primary and the secondary replicas for each chunk.

2) Master replies with the locations of the primary and secondary replicas. This information is cached.

---

# Writes (3)

.center.width-40[![](figures/lec8/gfs-write3.png)]

3) The client pushes the data to all replicas.
- Each chunkserver stores the data in an internal buffer.
- Each chunkserver sends back an acknowledgement to the client once the data is received.
- Data flow is decoupled control flow.

---

# Writes (4)

.center.width-40[![](figures/lec8/gfs-write4.png)]

4) Once all replicas have acknowledged, a **write request** is sent to the primary.
- This request identifies the data pushed earlier.
- The primary assigns consecutive serial numbers to all the mutations it receives, possibly from multiple clients.
    - This provides ordering.
- The primary applies the mutations, in the chosen order, to its local state.

---

# Writes (5)

.center.width-40[![](figures/lec8/gfs-write5.png)]

5) The primary forwards the write request to all secondary replicas.
- Mutations are applied locally in the serial order decided by the primary.

---

# Writes (6+7)

.center.width-40[![](figures/lec8/gfs-write67.png)]

6) The secondaries all reply to the primary upon completion of the operation.

7) The primary replies to the client.
- Errors are reported to the client.
    - The client request is considered to have failed.
    - The modified region is left in an **inconsistent state**.
    - The client handles errors by retrying the failed mutation.

---

# Appends



---

# Consistency model

- Relaxed consistency model.

- table

---

# Namespace management and locking

---

# Replica placement

---

# Creation, re-replication and rebalancing

---

# Garbage collection

---

# Stale replica detection

---

# Operation log

- The **operation log** is a persistent historical record of critical changes on metadata.
- Critical to the *recovery* of the system.
    - Master recovers its file system state by replaying the operation log.
    - Master periodically checkpoints its state to minimize startup time.
- Changes to metadata are only made visible to the clients **after** they have been written to the operation log.
- The operation log is *replicated* on multiple remote machines.
    - Before responding to a client operation, the log record must have been flushed locally and remotely.
- Serve as a **logical timeline** that defines the order of concurrent operations.

---

# Chunk locations

- Master does not keep a persistent record of chunk replica locations.
- Instead, it **polls** chunkservers about their chunks at startup.
- Master keeps up to date through *hearbeat* messages.
- A chunkserver has the **final word** over what chunks it stores.

<br><br><br><br><br><br><br><br><br><br><br><span class="Q">[Q]</span> What does this design decision simplify?

---

# Fault tolerance (master)

5.1

shadow replicas of master

---

# Fault tolerance (chunkserver)

---

# Data corruption

---

# Colossus

???

https://www.systutorials.com/3202/colossus-successor-to-google-file-system-gfs/

---

class: middle, center

# HDFS

---

# HDFS

---

# Summary

---

# References

- Ghemawat, Sanjay, Howard Gobioff, and Shun-Tak Leung. "The Google file system." ACM SIGOPS operating systems review. Vol. 37. No. 5. ACM, 2003.
- Shvachko, Konstantin, et al. "The hadoop distributed file system." Mass storage systems and technologies (MSST), 2010 IEEE 26th symposium on. IEEE, 2010.
- Claudia Hauff. "Big Data Processing, 2014/15. Lecture 5: GFS and HDFS".