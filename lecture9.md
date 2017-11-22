class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 9: Distributed databases and NoSQL

---

# Today

---

class: middle, center

# Databases

(Quick recap from [INFO0009: Databases](https://www.programmes.uliege.be/cocoon/cours/INFO0009-1.html))

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

# Relational data model (1)

- A simple but *general-purpose* model.
- Data is stored in **relations** (i.e., a collection of tables).
    - a *tuple* is a row of a relation.
    - an *attribute* is a column of a relation.
    - a *domain* is a set of legal *atomic* values for an attribute.
        - this can be used to enforce semantic constraints.

.center.width-60[![](figures/lec9/rel-db.gif)]

---

#  Relational data model (2)

- A **relation schema** is a list of attributes.
    - A schema is the blueprint that describes how the data is structured.
- A **relation** is a set of tuples for a given relation schema.
    - Each tuple in a relation is unique.
    - Uniqueness is often controlled through a (primary) *key* attribute.
- A *database schema* is a collection of relation schemas.
- **Relationships** between relations (tables) are defined by matching one or more attributes (usually, the keys).
    - 1-to-1 relationships
    - 1-to-many relationships
    - many-to-many relationships

---

# Querying data

- Data is retrieved, added or modified through an expressive *declarative query language*, **SQL**.
```SQL
SELECT EmployeeName, City FROM Employees;
```
    - Can be used to access data across one or more relations, with arbitrarily complex constraints.
    - Programmer specifies *what* answers a query should return, but **not how** the query is executed.
    - DBMS picks the best execution strategy, based on availability of indexes, data/workload, properties, etc.
- This provides *physical data independence*.
    - Applications should not worry about how data is physically structured and stored.
    - Applications instead work with a **logical** data model and a declarative query language.
    - Queries are often transparently optimized by a dedicated query processing engine.
- Single **most important reason** behind the success of DBMS today.

---

# Concurrency

- DBMSs are *multi-user*, which raises **concurrency** issues.
- Example:
    - Both Homer and Marge concurrently execute, on the same bank account:
```python
balance = get_balance_from_database()
if balance > amount:
            balance = balance - amount
            dispense_cash(amount)
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

**ACID** = key characteristics (most)
relational databases use to ensure modifications are saved in a
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

# Distributed relational databases

---

# Distributed relational databases

- A **distributed** database (DDBMS) is a database whose relations reside on different sites.
- Interface requirements:
    - Relational data model
    - ACID properties
    - Single system illusion

.center.width-60[![](figures/lec9/sites.png)]

<span class="Q">[Q]</span> How is this different from/similar to a distributed file system?

---

# Data placement

- The *data placement* strategy and its implications form the main part in the design of a DDBMS.
- Objective: distribute the relations over the sites.
    - Aim to improve reliability, availability, efficiency (e.g., reduced communication costs or better load balancing) and security.
- Key considerations:
    - **Fragmentation**: relations may be divided into a number of sub-relations which are distributed.
    - **Allocation**: each fragment is stored at site with optimal placement.
    - **Replication**: copy of fragment may be maintained at several sites.

---

# Fragmentation

- *Break* a relation into smaller relations or **fragments**, which are then distributed at different sites.
- Main types of fragmentation:
    - *Horizontal*: partition a relation along its tuples.
        - e.g., identify fragments to selection queries.
    - *Vertical*: partition a relation along its attributes.
        - e.g., identify fragments to projection queries.
    - *Mixed*: partition horizontally and vertically.

.center.width-80[![](figures/lec9/fragmentation.jpg)]

---

# Correctness rules of fragmentation

A fragmentation strategy should satisfy the following properties:
- *Completeness*: If a relation $R$ is decomposed into fragments $R_1, ..., R_n$, each data item that can be found in $R$ must appear in a least one fragment.
- *Reconstruction*: Must be possible to define a relation operation that will reconstruct $R$ from its fragments.
    - **Union** to combine horizontal fragments
    - **Join** to combine vertical fragments
- *Disjointness*: If data item $d$ appears in fragment $R\_i$, then it should not appear in any other fragment (at the exception for primary keys).
    - For horizontal fragmentation, data item is a tuple.
    - For vertical fragmentation, data item is an attribute.

---

# Allocation

- Ideally, fragments should be **allocated** such that queries that are frequently performed locally at sites are fast.
    - e.g., store tuples of Belgian employees at Brussels' site, but tuples of Japanese employees at Tokyo's.
- *Optimization problem*:
    - Givens:
        - fragments $f_1, ..., f_n$
        - sites $s_1, ..., s_m$
        - applications $q_1, ..., q_k$
    - Find the optimal assignment of fragments to sites such that the total cost of all applications is minimized and the performance is maximized.
        - Application costs: communication, storage, processing.
        - Performance: response time, throughput.
    - Constraints: per site constraints (storage and processing)
    - Problem is in general NP-complete, but good heuristics exist.
        - Reduce to a knapsack problem.
---

# Replication

- Storing a same fragment at distinct sites increases **availability** and **efficiency**.
- Replication modes:
    - *fully replicated*: each fragment at each site.
    - *partially replicated*: each fragment at one or more sites.
- Rule of thumb: if read-only queries / update queries $\geq 1$, then replication is advantageous, otherwise it may cause problems.
- The optimal partial replication policy can be determined jointly with the allocation problem.

---

# Distributed query processing

- For centralized systems, all data is local and queries are mainly optimized to limit disk accesses.
- In DDBMSs, the data is distributed across several sites. This has the following consequences:
    - The query processing engine must *communicate* with all sites holding fragments involved in the query.
        - The cost of data transmission becomes a dominant factor when optimizing the query.
    - The engine must **orchestrate** the execution of sub-queries to compute the original query.
    - Independent sub-queries can be scheduled *concurrently*.

---

# Non-joins

.center.width-50[![](figures/lec9/query-table.png)]

```SQL
SELECT AVG(S.age)
FROM Sailors AS S
WHERE S.rating > 3 AND
      S.rating < 7
```
- Horizontal fragmentation: Tuples with ratings $< 5$ at Brussels, $\geq 5$ at Tokyo.
    - Must compute `SUM(S.age)` and `COUNT(s.age)` at both sites, before being recombined.
    - If the `WHERE` clause contained just `S.rating > 6`, then the query could processed at one site only.
- Vertical fragmentation:
    - Must reconstruct relation by join on `tid`, then evaluate the query.

---

# Joins

- Joins in DDBMSs can be very **expensive** if relations are stored at different sites.
- Consider three relations `account`, `depositor` and `branch`.
    - We want to compute their join `account`⋈`depositor`⋈`branch`.
        - `account` is stored at site 1.
        - `depositor` is stored at site 2.
        - `branch` is stored at site 3.
    - A query issued at site 1 must produce a result at site 1.

---

# Possible strategies

- Ship copies of all three relations to site 1 and process the query locally.
- Ship a copy of `account` to site 2, compute `temp1`=`account`⋈`depositor`.
  Ship `temp1` from site 2 to site 3, compute `temp2`=`temp1`⋈`branch`.
  Ship `temp2` to site 1.

<span class="Q">[Q]</span> Can we do better?

---

# Semijoins

- We do not need to exchange the *whole* relations! Semijoins are sufficient.
    - Project `depositor` onto join columns with `branch` and ship to site 3.
    - At site 3, join the projection with `branch`.
      Project the resulting relation onto the join columns with `account` and ship to site 1.
    - At site 1, join the projection with `account`.
- Tradeoff the cost of computing and shipping projection for cost of shipping full relation.

---

# Updating distributed data

- *Synchronous replication*:
- *Asynchronous replication*:

---

# Distributed transactions


---

# Two-phase commit


---

# Case study: Spanner

https://cloud.google.com/spanner/

---

class: middle, center

# NoSQL

---

# Structured vs. unstructured data

---

# DHT

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

dremel

---

# Case study: Bigtable

---

# Case study: Cassandra

---

# Case study: Kudu

---

# Summary

---

# References

- Slides inspired from "[CompSci 316: Introduction to Database Systems](https://sites.duke.edu/compsci316_01_s2017/)", by Prof. Sudeepa Roy, Duke University.
