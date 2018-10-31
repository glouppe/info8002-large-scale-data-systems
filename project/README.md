# KeyChain

## Table of contents

- [Introduction](#introduction)
- [Instructions](#instructions)
  - [Group formation](#group-formation)
  - [Tips](#general-tips-and-guidelines)
- [Evaluation](#evaluation)

---

## Introduction

The main objective of this project is to implement your own decentralized Blockchain [key-value store](https://en.wikipedia.org/wiki/Key-value_database).

---

## Instructions

### Group formation

### General tips and guidelines

---

## Evaluation

This project is a requirement to pass INFO8002, and **must** be completed and submitted with all deliverables to the [Montefiore submission system](https://submit.montefiore.ulg.ac.be/) by the **hard deadline** of `21/12/2018 23:59`. You are allowed to implement the project by yourself, or in groups with a maximum of *3* students (see [group formation](#group-formation)).

We expect the following deliverables;

- An **implementation** with the following requirements:
  * a Python implementation,
  * Blockchain and Block architecture with accompanying consensus rules,
  * proof of work (PoW) with a parameterizable difficulty level,
  * abstraction layer for the top-level application:
    - `put(key, value)`
    - `get(key)`
    - `get_all(key)`
  * code the reproduce the experiments and the associated plots.
- A **report** in PDF format that must include:
  * a detailed description of the individual components in your solution,
  * a discussion of the consequences and scalability of your broadcast implementation,
  * a discussion about the applicability of Blockchain to this problem,
  * an experiment showning the transaction throughput with respect to the difficulty level,
  * an experiment demonstrating the resistance against Bryzantine attacks under different difficulty levels (e.g., double spending with 51% attack).

---
