# KeyChain

The objective of this project is to implement your own decentralized Blockchain [key-value store](https://en.wikipedia.org/wiki/Key-value_database).

This project is a requirement to pass the course. It  **must** be completed and submitted with all deliverables to the [Montefiore submission system](https://submit.montefiore.ulg.ac.be/) by the **hard deadline** of **December 21, 2018 23:59**.

You are allowed to implement the project by yourself, or in groups with a maximum of *3* students.

## Implementation

You are tasked with the implementation of a **distributed key-value store**. This data system should provide a service to store key-value pairs while guaranteeing their persistence and integrity, i.e. such that the historical content of the key-value store cannot be altered by any third party.

Your architecture should be designed around three main components:
- a top-level store component that interfaces with the user-level application.
  The top-level API should provide the following methods:
    - `put(key, value)`:
    Stores the `value` with the associated `key`.
        - If a value for `key` already exists in the store, then a new version of the pair is created with the value `value`.
        - Please make note of the fact that the `put` operation doesn't necessarily delivers after it has been completed. It may therefore be a good idea to add a `callback` procedure (or a different mechanism) that is called whenever the key has been added to the system, or if a failure occurred.
    - `retrieve(key)`:
    Searches the store for the latest value with the specified key.
    - `retrieve_all(key)`:
    Retrieves all values historically recorded in the store for the specified key.
- a blockchain component that takes care of the decentralized and persistent storage.
- a broadcast component for communication between nodes.

Additional requirements:
- Your system should run in a distributed and decentralized fashion, on multiple machines.
- The store should be resilient to (one or multiple) faults.
- Your implementation must be able to handle conflicts.
- In your blockchain implementation, proof of work should have a parameterizable difficulty level.
- Your broadcast implementation should be sufficiently reliable while remaining efficient (pick wisely).
- You must provide a bootstrapping procedure for new nodes joining the network.

Beyond this coarse structure, **you are free** to design and implement this project in any way you consider appropriate.

#### Coding guidelines

- Code should be in Python, with a proper modular implementation.
- Style, documentation and unit tests will be evaluated.
- You can bootstrap your project from the stub provided in `/code/`. You are free to modify, remove or extend any part of it.
- We recommend network communication to be implemented through a REST API, in order to simplify development.
- Provide instructions and code for running your implementation of the key-value store, as well as for reproducing all experiments and results (including plots, if any).
- Do not over-engineer. We expect a working proof-of-concept, not a full fledged professional solution. Prefer simplicity over complexity.


## Report

Your project must comes with a written **report** (in PDF) that includes:
* A detailed description of your general architecture, its individual components and their interactions. Specify clearly your set of assumptions.
* A discussion of the consequences and scalability of your broadcast implementation.
* A discussion about the applicability of a blockchain to this problem.
* An experiment demonstrating the resistance of the key-value store against faults.
* An experiment showing the transaction throughput with respect to the difficulty level.
* An experiment demonstrating a 51% attack by rewriting an older version of a key.

Experimental results should all come with a critical discussion.
