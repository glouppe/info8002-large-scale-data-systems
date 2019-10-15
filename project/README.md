# DFTFS
> Distributed Fault-Tolerant File System

## Introduction
The main objective of this project is to implement a distributed and fault-tolerant file system.
This implies that if one or more processes fail, the normal operation of the file-system and its
interface should be guaranteed.

This project is a requirement to pass the course. It must be completed and submitted with all deliverables to the Montefiore submission system by the hard deadline of **December 20, 2019 23:59**.
The project can be completed in a group with a maximum of 3 students.

## Implementation
We give you the complete freedom to implement and design the file
system. However, the following interfaces should be implemented:

> **`put(path, bytes)`**

Puts the bytes on the specified path. This method will raise an exception when a file is present on the specified path.

> **`copy(source_path, destination_path)`**

This will copy the file at the specified source path, to the specified destination path. If the source path not exists, or the destination path is not available an exception should be raised.

> **`get(path)`**

Returns all bytes of the file present at the specified path. If the path does not exist, an exception should be raised.

> **`exists(path)`**

Checks if a file exists at the specified path. Returns “true” (not a string) if a file is present at the specified location, false otherwise.
Other methods are most likely required, but these are the endpoints available to the end-user.

**Data should NOT be replicated to all processes** (assume the data is too large).
Doing so will result in a fail for this project.

## Deliverables

We would like you to hand in the following deliverables:

- A distributed **implementation** with the following requirements:
  - Bash script to start your distributed file system.
    The bash script should print the `pid`’s (process identifiers)
    of every process you start.
  - The following HTTP (REST) endpoints:
    - `PUT` **/path** (implements **put(path, bytes)**).
    - `GET` **/path** (implements **get(path)**).
    - `GET` **/exists** (implements **exists(path)**, returns `0` or `1`).
    - `POST` **/copy** (with arguments `source_path` and `destination_path`)
  - It is preferable that these HTTP endpoints have proper HTTP response code (e.g., HTTP 200 for success).
  - Resistant to failures (your assumptions, e.g., number of failures). The REST endpoints should remain functional whenever I kill a process.
  - A script demonstrating the fault-tolerance of your storage (you should be able to retrieve files while killing processes).
- A **report** in PDF format which must include:
  - A clear description of your architecture and assumptions.
  - A discussion on the fault-tolerance of your system and safeguards when performing high-level operations (e.g., what happens if I use put and a worker fails)? Additionally, what kind of fault-tolerance can you deliver?
  - A discussion on the implementation of `ls` (list files) and `rm` (remove files) within your framework.
  - An experiment demonstrating and discussing the fault-tolerance of your system.

## General tips and coding guidelines

- You are free to implement your project in any programming language, as long as it comes with a proper modular implementation and an abstraction layer for the top-level application.
- You can bootstrap your project from the stub provided in `/code/`. You are free to modify, remove or extend any part of it.
- We recommend network communication to be implemented through a REST API (e.g., using `flask` and `requests` in Python), in order to simplify development.
- Provide instructions and code for running your implementation of the distributed file system, as well as for reproducing all experiments and results (including plots, if any).
- Do not over-engineer. We expect a working proof-of-concept, not a full fledged professional solution. Prefer simplicity over complexity.
