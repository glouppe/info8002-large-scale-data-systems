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
- Files are *large* (multi-GB files are the norm) and their number is limited (millions, not billions).
- Two main types of reads:
    - *large streaming reads*
    - *small random reads*
- Workloads with **sequential writes** that *append* data to files.
- Once written, files are *seldom modified* ($\neq$ append) again.
    - Random modification in files is possible, but not efficient in GFS.
- Well-defined **semantics** for multiple clients that *concurrently* append to the same file.
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

# Disclaimer

- GFS (and HDFS) are **not a good fit** for:
    - Low latency data access (in the ms range).
        - Solution: distributed databases, such as HBase.
    - Many small files.
    - Constantly changing data.
- Not all details of GFS are public knowledge.

---

# How would you design a DFS?

.grid[
.col-1-2[
- We want *single system illusion* for data storage.
- Although data is too large be stored in a single system.
- Hardware **will** fail.
]
.col-1-2[
![](figures/lec8/google-first-server.jpg)
.caption[Google first server]
]
]

---

# Architecture

.center.width-100[![](figures/lec8/gfs-architecture.png)]

- A single **master** node.
- Multiple *chunkservers* storing the data.
- Multiple clients.

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

# Reading (1)

.center.width-100[![](figures/lec8/gfs-read1.png)]

1) The GFS client translates filename and byte offset specified by the application into a *chunk index* within the file. A request is sent to master.

---

# Reading (2)

.center.width-100[![](figures/lec8/gfs-read2.png)]

2) Master replies with chunk handle and locations of the replicas.

---

# Reading (3+4)

.center.width-100[![](figures/lec8/gfs-read3.png)]

3) The client caches this information using the file name and chunk index as the key.
- Further reads of the same chunk requires no more client-master interaction, until the cached information expires.

4) The client sends a request to one of the replicas, typically the closest.

---

# Reading (5)

.center.width-100[![](figures/lec8/gfs-read4.png)]

5) The contacted chunkserver replies with the data.

---

# Chunk sizes

- Default size = 64MB.
- Advantages of large (but not too large) chunk size:
    - **Reduced** need for client/master interaction.
    - 1 request per chunk suits the target workloads.
    - Client can cache *all the locations* for a multi-TB working set.
    - **Reduced size** of metadata on master (kept in memory).
- Disadvantage:
    - A chunkserver can become a **hotspot** for popular files.

<br><br><br><br><br><br><br><span class="Q">[Q]</span> How to fix the hotspot problem?

---

# Chunk locations

- Master does not keep a persistent record of chunk replica locations.
- Instead, it **polls** chunkservers about their chunks at startup.
- Master keeps up to date through *hearbeat* messages.
- A chunkserver has the **final word** over what chunks it stores.

<br><br><br><br><br><br><br><br><br><br><br><span class="Q">[Q]</span> What does this design decision simplify?

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

# Consistency model

---

# Writing

3.1 3.2


---

# Namespace management and locking

---

# Replica placement

---

# Garbage collection

---

# Stale replica detection

---

# Fault tolerance

5.1

shadow replicas of master

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
