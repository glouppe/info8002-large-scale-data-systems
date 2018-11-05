# KeyChain

The objective of this project is to implement your own decentralized Blockchain [key-value store](https://en.wikipedia.org/wiki/Key-value_database).

- [Organization](#organization)
- [Implementation](#implementation)
- [Report](#report)

## Organization

This project is a requirement to pass the course, and **must** be completed and submitted with all deliverables to the [Montefiore submission system](https://submit.montefiore.ulg.ac.be/) by the **hard deadline** of  December 21, 2018 23:59.
You are allowed to implement the project by yourself, or in groups with a maximum of *3* students.

## Implementation

You are tasked with the implementation of a distributed key-value store. This module should provide a service to store `(key, value)` pairs while guaranteeing their persistence and integrity.

Your implementation should be designed around three main components:
- a top-level store component that interfaces with the main application.
  The top-level API should provide the following methods:
    - `put(key, value)`:
    Stores the `value` with the associated `key`. If a value for `key` already exists in the store, then a new version of the pair is created with the value `value`.
    Please make note of the fact that the `put` operation doesn't necessarily delivers after it has been completed. It may therefore be a good idea to add a `callback` procedure (or a different mechanism) that is called whenever the key has been added to the system, or if a failure occurred.
    - `retrieve(key)`:
    Searches the store for the latest value with the specified key.
    - `retrieve_all(key)`:
    Retrieves all values historically recorded in the store for the specified key.
- a blockchain component that takes care of the distributed and persistent storage.
- a broadcast component for communication between nodes.

Additional requirements:
- In your blockchain implementation, proof of work should have a parameterizable difficulty level.
- Your broadcast implementation should be sufficiently reliable while remaining efficient.
- You must provide a bootstrapping procedure for new nodes joining the network.
- Your implementation must be able to handle conflicts.
- The store should be resilient to faults.

Beyond this coarse structure, you are **free** to design and implement this project in any way you consider appropriate. However, when in doubt, keep it stupid simple (KISS).

Coding guidelines:
- Code should be in Python.
- You code bootstrap your project from the stub provided in `/code/`. You are free to modify or extend any part of it.
- The blockchain and broadcast components should both be running behind a REST API.
- Provide instructions and code for running your system, as well as for reproducing all experiments and results (including plots, if any).


## Report

Your project must comes with a written **report** in PDF format that includes:
* A detailed description of the individual components in your solution, along with your system assumptions.
* A discussion of the consequences and scalability of your broadcast implementation.
* A discussion about the applicability of Blockchain to this problem.
* An experiment showing the transaction throughput with respect to the difficulty level.
* An experiment demonstrating a 51% attack by rewriting an older version of a key.
* An experiment demonstrating the resistance of the key-value store against faults.

Experimental results should all come with a critical discussion.
