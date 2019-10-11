# DFTFS
> Distributed Fault-Tolerant File System

## Introduction
The main objective of this project is to implement a distributed and fault-tolerant file system.
This implies that if one or more processes fail, the normal operation of the file-system and its
interface should be guaranteed. We give you the complete freedom to implement and design the file
system. However, the following interfaces should be implemented:


Other methods are most likely required, but these are the endpoints available to the end-user.
**Data should NOT be replicated to all processes** (assume the data is too large).
Doing so will result in a fail for this project.


We would like you to hand in the following deliverables:

- An **implementation** with the following requirements:
  - Bash script to start your distributed file system.
    The bash script should print the `pid`’s (process identifiers)
    of every process you start.
