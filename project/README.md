# KeyChain

## Table of contents

- [Introduction](#introduction)
- [Instructions](#instructions)
  - [Group formation](#group-formation)
- [Evaluation](#evaluation)

---

## Introduction

The main objective of this project is to implement your own decentralized Blockchain [key-value store](https://en.wikipedia.org/wiki/Key-value_database).

---

## Instructions

### Group formation

Please register your group at the [Montefiore submission system](https://submit.montefiore.ulg.ac.be/), also if you are working alone.

### Evaluation

This project is a requirement to pass INFO8002, and **must** be completed and submitted with all deliverables to the [Montefiore submission system](https://submit.montefiore.ulg.ac.be/) by the **hard deadline** of `21/12/2018 23:59`. You are allowed to implement the project by yourself, or in groups with a maximum of *3* students (see [group formation](#group-formation)).

We expect the following deliverables;

- An **implementation** with the following requirements:
  * a Python implementation,
  * Blockchain and Block architecture with accompanying consensus rules,
  * a bootstrapping procedure for new nodes joining the network,
    - New nodes have to "download" the Blockchain from peers.
  * proof of work (PoW) with a parameterizable difficulty level,
  * abstraction layer for the top-level application:
    - `put(key, value)`
    Stores the `value` with the associated `key` in the Blockchain. Please make note of the fact that the `put` operation doesn't necessarily deliveres after it has been completed. It may therefore be a good idea to add a `callback` procedure (or a different mechanism) that is called whenever the key has been added to the chain, or if a failure occurred (i.e., duplicate key in the same block). This serves the purpose of the `deliver` operation from the lectures.
    - `get(key)`
    Searches the Blockchain for the latest value with the specified key.
    - `get_all(key)`
    Retrieves all values from the Blockchain with the specified key.
  * code the reproduce the experiments and the associated plots,
  * broadcast implementation to dissipate information through your Blockchain network (choose wisely),
- A **report** in PDF format that must include:
  * a detailed description of the individual components in your solution,
  * a discussion of the consequences and scalability of your broadcast implementation,
  * a discussion about the applicability of Blockchain to this problem,
  * an experiment showning the transaction throughput with respect to the difficulty level,
  * an experiment demonstrating the resistance against Bryzantine attacks under different difficulty levels (e.g., double spending with 51% attack).

---
