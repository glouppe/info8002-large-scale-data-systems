class: middle, center, title-slide

# Large-scale Distributed Systems

Fall 2017

---

# Organization

## Logistics
- Prof. Gilles Louppe ([g.louppe@ulg.ac.be](mailto:g.louppe@ulg.ac.be))
- Teaching assistant: Joeri Hermans ([joeri.hermans@doct.ulg.ac.be](mailto:joeri.hermans@doct.ulg.ac.be))

.pull-right[![Textbook](./figures/textbook.jpg)]
## Notes
Rachid Guerraoui, Luis Rodrigues, "Introduction to Reliable Distributed Programming", Springer. (*optional*)

Slides are partially adapted from:
- [CSE 486/585 Distributed systems](https://www.cse.buffalo.edu/~stevko/courses/cse486/spring16/schedule.html) (University at Buffalo)
- [CS425 Distributed systems](https://courses.engr.illinois.edu/cs425/fa2017/lectures.html) (University of Illinois UC)
- ID2203 Introduction to Distributed Systems (KTH).

---

# Philosophy

## Solid ground

- Understand the **foundational principles** of distributed systems, on top of
which distributed *databases* and *computing* systems are operating.

## Practical

- Exposition to *industrial software*.
- Fun and challenging course project.

## Critical thinking

- Assess the benefits and disadvantages of distributed systems.
- No hype!

---

class: middle, center

# Outline

---

class: middle, center

# I. Foundations

---

# 1. Distributed systems

- Introduction to distributed systems
- Outline
- Networking basics

---

# 2. Basic abstractions

- Distributed computation model
- Abstracting processes
    - Failures
- Abstracting communication
- Abstracting time
    - Timing assumptions
    - Failure detection
    - Leader election
- Distributed abstractions

---

# 3. Reliable delivery

- Reliable multicast

???

- Gossiping

---

# 4. Shared memory

- Shared memory

???

- Global states

---

# 5. Consensus

- Consensus
- Impossibility result
- Paxos
- Replication (total order broadcast)

???

- Possibly split into two parts.
- Firefly consensus, impossibility

---

class: middle, center

# II. Computing paradigms for data science

---

# 6. Map Reduce

- Concept
- Case study: Hadoop

---

# 7. Computational graph systems

- Concept
- Static vs. dynamic graphs
- Optimization
- Case studies: Spark, Tensorflow, PyTorch

---

# 8. Data science on a budget

- A lot can be done using a laptop only
- Algorithmic solutions to large-scale data science problems

---

class: middle, center

# III. Distributed data storage

---

# 9. Distributed file systems

- Architecture
- RPC
- Scalability (partitioning)
- Case study: GFS, HDFS

---

# 10. Key-value stores / NoSQL

- Structured vs. Unstructured databases
- DHT
- Case study: Amazon Dynamo, Apache Cassandra

---

# 11. Block chain

- Concept
- Case study: Bitcoin

---

class: middle, center

# Projects

---

XXX
