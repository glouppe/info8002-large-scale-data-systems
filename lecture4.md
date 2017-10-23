class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 4: Shared memory

---

# Today

- How do you *share resources*?
- Can we build the *illusion of single storage*?
    - While replicating data for **fault-tolerance** and **scalability**?
    - While maintaining **consistency**?

---

# Real shared memory

.center.width-60[![](figures/lec4/real-sm.gif)]

- In a multiprocessor machine, processors typically communicate through **shared memory** provided at the hardware level.
    - e.g., shared blocks of RAM that can be accessed by distinct CPUs.
- Shared memory can be viewed as an *array of registers* to which processors can *read* or *write*.
- Shared memory systems are *easy to program* since all processors share a single view of the data.

---

# Shared memory emulation

We want to **simulate** a *shared memory abstraction* in a distributed system, on top of message passing communication.

Why?
- Enable shared memory algorithms without being aware that processes are actually communicating by exchanging messages.
    - This is often much easier to program.
- Equivalent to **consistent data replication** across nodes.

---

# Data replication

- Why **replicating data** across nodes? Shared data allows to:
    - Reduce network traffic
    - Promote increased parallelism
    - Be robust against failures
    - Result in fewer page faults
- Applications:
    - distributed databases
    - distributed file systems
    - distributed cache
    - ...
- Challenges:
    - Consistency in presence of *failures*.
    - Consistency in presence of *concurrency*.

---

# Read/Write registers

- A **register**  represents each memory location.
- A register contains only positive integers and is initialized to $0$.
- Registers have two *operations*:
    - $\text{read}()$: return the current value of the register.
    - $\text{write}(v)$: update the register to value $v$.
- An operation is **not instantaneous**:
    - It is first *invoked* by the calling process.
    - It computes for some time.
    - It returns a *response* upon completion.

.width-100[![](figures/lec4/rw-operations.png)]

---

# Definitions

- In an execution, an operation is
    - *completed* if both invocation and response occurred.
    - *failed* if invoked but not no response was received.
- Operation $o_1$ *precedes* $o_2$ if response of $o_1$ precedes the invocation of $o_2$.
- Operations  $o_1$ and  $o_2$ are *concurrent* if neither precedes the other.
- $(1,N)$ register: 1 designated writer, multiple readers.
- $(M,N)$ register: multiple writers, multiple readers.

---

class: middle, center

# Regular registers

---

# Regular registers

.center[![](figures/lec4/regular-register.png)]

---

# Regular register example (1)

.width-100[![](figures/lec4/regular-example1.png)]

<span class="Q">[Q]</span> Regular or non-regular?

???

Non-regular.

---

# Regular register example (2)

.width-100[![](figures/lec4/regular-example2.png)]

<span class="Q">[Q]</span> Regular or non-regular?

???

Regular.

---

# Regular register example (3)

.width-100[![](figures/lec4/regular-example3.png)]

<span class="Q">[Q]</span> Regular or non-regular?

???

Regular.

Not a single storage illusion!

---

# Centralized algorithm

- Designates one process as the **leader**.
    - E.g., using the leader election abstraction.
- To $\text{read}()$:
    - Ask the leader for latest value.
- To $\text{write}(v)$:
    - Update leader's value to $v$.

<span class="Q">[Q]</span> Problem? **Does not work if leader crashes!**

---

# Decentralized algorithm (bogus)

- Intuitively, make an algorithm in which
    - A $\text{read}()$ reads the local value.
    - A $\text{write}(v)$ writes to all nodes.
- To $\text{read}()$:
    - Return local value.
- To $\text{write}(v)$:
    - Update local value to $v$.
    - Broadcast $v$ to all (each node locally updates).
    - Return.

<span class="Q">[Q]</span> Problem?

---

# Decentralized algorithm (bogus) example

.width-100[![](figures/lec4/bogus-example.png)]

.center[**Validity is violated!**]

---

# Read-one Write-all algorithm

- Bogus algorithm modified.
- To $\text{read}()$:
    - Return local value.
- To $\text{write}(v)$:
    - Update local value to $v$.
    - Broadcast $v$ to all (each node locally updates).
    - **Wait for acknowledgement from all correct nodes.**
        - Require a perfect failure detector (fail-stop).
    - Return.

---

# Read-one Write-all algorithm

.center.width-70[![](figures/lec4/r1wN-impl.png)]

---

#  Read-one Write-all example

.width-100[![](figures/lec4/r1wN-example.png)]

.center[Validity is no longer violated because the write response has been postponed.]

---

# Quorum principle

- Can we implement a regular register in *fail-silent*?
- **Quorum principle**:
    - Assume a majority of correct nodes.
    - Divide the system into two overlapping *majority quorums*.
        - i.e., each quorum  counts at least $\lfloor \frac{N}{2} \rfloor + 1$ nodes.
    - Always write to and read from a majority of nodes.
    - At least one node knows the most recent value.

.center.width-50[![](figures/lec4/quorum.png)]

---

# Majority voting algorithm

.center.width-70[![](figures/lec4/majority-voting-impl1.png)]

---

.center.width-70[![](figures/lec4/majority-voting-impl2.png)]

---

class: middle, center

# Atomic registers
towards single storage illusion

---

# Sequential consistency

An operation $o_1$ *locally precedes* $o_2$ in $E$ if $o_1$ and $o_2$ occur at the same node and $o_1$ precedes $o_2$ in $E$.

An execution $E$ is **sequentially consistent** if an execution $F$ exists such that:
- $E$ and $F$ contain the same events;
- $F$ is sequential;
- Read responses have value of the preceding write invocation in $F$;
- If $o_1$ locally precedes $o_2$ in $E$, then $o_1$ locally precedes $o_2$ in $F$.

---

# Example (1)

.width-100[![](figures/lec4/atomic-example1.png)]

Sequential consistency **disallows** such execution.

---

# Example (2)

.width-100[![](figures/lec4/atomic-example2.png)]

Sequential consistency *allows* such execution.

---

# $(1, N)$ atomic registers

- *Linearizability*:
    - Read operations appear as if **immediately** happened at all nodes at time between invocation and response.
    - Write operations appear is if **immediately** happened at all anode at time between invocation and response.
    - Failed operations appear as
        - completed at every node, XOR
        - never occurred at any node.
    - The hypothetical serial execution is called a *linearization* of the actual execution.
- *Termination*:
    - If node is correct, each read and write operation eventually completes.

---

# Example (1)

.width-100[![](figures/lec4/atomic-example1.png)]

Linearizability **disallows** such execution.

---

# Example (2)

.width-100[![](figures/lec4/atomic-example2.png)]

Linearizability **disallows** such execution.

---

# $(1, N)$ atomic registers

.center[![](figures/lec4/atomic-register.png)]

<span class="Q">[Q]</span> Show that linearizability is equivalent to validity + ordering.

---

# Atomic register example (1)

.width-100[![](figures/lec4/linearization-example1.png)]

<span class="Q">[Q]</span> Atomic? **No**, not possible to find linearization points.

---

# Atomic register example (2)

.width-100[![](figures/lec4/linearization-example2.png)]

<span class="Q">[Q]</span> Atomic? *Yes*

---

# Atomic register example (3)

.width-100[![](figures/lec4/linearization-example3.png)]

<span class="Q">[Q]</span> Atomic? *Yes*

---

# Regular but not atomic

.width-100[![](figures/lec4/regular-not-atomic.png)]

<span class="Q">[Q]</span> Atomic? **No**. Regular? *Yes*, using majority voting.

---

class: smaller

# Implementation of $(1,N)$ atomic registers

Idea:
- When reading, write back the value that is about to be returned.
- Maintain a local timestamp $ts$ and its associated value $val$.
- Overwrite the local pair only upon a write operation of a more recent value.

.center.width-70[![](figures/lec4/riwa.png)]

---

# Read-Impose Write-all algorithm

.center[![](figures/lec4/riwa-impl1.png)]

---

.center[![](figures/lec4/riwa-impl2.png)]

<span class="Q">[Q]</span> Show the algorithm is correct.

<span class="Q">[Q]</span> How to adapt to fail-silent? **Read-Impose Write-Majority**

---

# Correctness

- *Ordering*: if a read returns $v$ and a subsequent read returns $w$, then the write of $w$ does not precede the write of $v$.
    - $p$ writes $v$ with timestamp $ts_v$.
    - $p$ writes $w$ with timestamp $ts_w > ts_v$.
    - $q$ reads the values the $w$.
    - some time later, $r$ invokes a read operation.
    - when $q$ completes its read, all correct processes have a timestamp $ts \geq ts_w$.
    - there is no way for $r$ to changes its value back to $v$ after this because $ts_v < ts_w$.

<span class="Q">[Q]</span> Show that the termination and validity properties are satisfied.

---

# $(N, N)$ atomic registers

.center[![](figures/lec4/nn-atomic-register.png)]

---

# $(N, N)$ atomic registers

- How do we handle **multiple writers**?
- Read-Impose Write-all does not support multiple writers:
    - Assume $p$ and $q$ both store the same timestamp $ts$ (e.g., because of a preceding completed operation).
    - When $p$ and $q$ proceed to write, different values would become associated with the same timestamp.
- Fix:
    - Together with the timestamp, pass and store the identity $pid$ of the process that writes a value $v$.
    - Determine which message is the latest
        - by comparing timestamps,
        - by breaking ties using the process IDs.


<span class="Q">[Q]</span> How many messages are exchanged per read and write operations?

<span class="Q">[Q]</span> Can we similarly fix Read-Impose Write-Majority?

---

# Simulating message passing?

- As we saw, we can simulate shared with message passing.
    - A majority of correct nodes is all that is needed.
- Can we *simulate message passing* in shared memory?
    - Yes: use one register $pq$ for every channel.
        - Modeling a directed channel from $p$ to $q$.
    - Send messages by appending to the right channel.
    - Receive messages by busy-polling incoming "channels".
- Shared memory and message passing are **equivalent**.

---

# Summary

- Shared memory registers form a **shared memory abstraction** with read and write operations.
    - Consistency of the data is guaranteed, even in the presence of failures and concurrency.
- Regular registers:
    - Bogus algorithm (does not work)
    - Centralized algorithm (if no failures)
    - Read-One Write-All algorithm (fail-stop)
    - Majority voting (fail-silent)
- Atomic registers:
    - Single writers
    - Multiple writers
