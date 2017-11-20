class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 9: Distributed databases and NoSQL

---

# Today

---

class: middle, center

# Databases

Quick recap from [INFO0009 Database (general organisation)](https://www.programmes.uliege.be/cocoon/cours/INFO0009-1.html)

---

# Databases

From Oxford dictionary:
- *Database*: an organized body of related information.
- *Database system*, *Database management system* (DBMS): a software system that facilitates the creation and maintenance and use of an electronic database

What do you want from a DBMS?
- *Persistence*: Keep data around.
- *Queries*: answer questions about data.
- *Updates*: add, modify, delete data.

<span class="Q">[Q]</span> Which database systems do you know?

---

# Relational databases

- A simple but general-purpose model: data is stored in **relations** (tables).
- A *declarative query language*: SQL.
```SQL
SELECT CustomerName, City FROM Customers;
```
    - Programmer specifies *what* answers a query should return, but **not how** the query is executed.
    - DBMS picks the best execution strategy, based on availability of indexes, data/workload, properties, etc.
- This provides *physical data independence*.
    - Applications should not worry about how data is physically structured and stored.
    - Applications instead work with a **logical** data model and a declarative query language.
- Single most important reason behind the success of DBMS today.

---

# Concurrency

- DBMS are *multi-user*.
- Example. Both Homer and Marge **concurrently** execute:
```python
balance = get_balance_from_database()
if balance > amount:
        balance = balance - amount
        dispense_cash()
        store_into_database(balance)
```
    - Homer at ATM1 withdraws $100.
    - Marge at ATM2 withdraws $200.
    - Initial balance = $400.
    - What is the final balance?

<span class="Q">[Q]</span> Haven't we already studied a similar problem?

---

# Fault-tolerance and recovery

- Example: balance transfer.
    - decrement the balance of account $X$ by $100.
    - increment the balance of account $Y$ by $100.
- Scenario 1: Power goes out after the first instruction.
- Scenario 2: DBMS buffers and updates data in memory (for efficiency), but power goes out before they are written back to disk.
- How can we deal with these **failures**?

---

# ACID

The **ACID** database properties define the key characteristics (most)
relational databases use to ensure database modification are saved in a
consistent, safe, and robust manner.
- *Atomic*: In a transaction with two or more pieces of information, either all of the pieces are committed or none are.
- *Consistent*: A transaction either creates a new valid state of data, or, if any failure occurs, returns all data to its state before the transaction was started.
- *Isolation*: A transaction in process and not yet committed must remain isolated from any other transaction.
- *Durable*: Committed data is saved by the system such that, even in the event of a failure and system restart, the data is available in its correct state.

<span class="Q">[Q]</span> Don't some of these properties look familiar?

---

# Performance

- DBMSs are designed to store **massive** amounts of data (TB, PB).
- High throughput is desired (thousands to millions transactions/hour).
- High availability ($\geq$ 99.999%).

<span class="Q">[Q]</span> How can we address these issues, at large-scale?

---

class: middle, center

# Distributed databases

---

# Distributed databases

---

# Architectures

---

# Fragmentation

---

# Replication

---

# Distributed queries

---

# Joins

---

# Semijoins

---

# Updating distributed data

---

# Distributed transactions

---

# Deadlocks

---

# Two-phase commit

---

# Three-phase commit

---

# Case study: Spanner

https://cloud.google.com/spanner/

---

class: middle, center

# NoSQL

---

# Structured vs. unstructured data

---

# NoSQL

---

# BASE

---

# CAP theorem

---

# Choices in NoSQL systems

concurrency control

---

# Choices in NoSQL systems

data storage medium

---

# Choices in NoSQL systems

replication

---

# Choices in NoSQL systems

transactions

---

# Comparison

---

# Data store categories

---

# RDBMS benefits

---

# NoSQL benefits

---

# Column store

---

# Case study: Bigtable

---

# Case study: Cassandra

---

# Summary

---

# References

- Slides inspired from "[CompSci 316: Introduction to Database Systems](https://sites.duke.edu/compsci316_01_s2017/)", by Prof. Sudeepa Roy, Duke University.
