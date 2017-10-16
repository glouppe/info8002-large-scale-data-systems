class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 4: Shared memory

---

# Today

XXX

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
- Equivalent to **consistent data replication** across nodes.
    - for **fault-tolerance**
    - for **scalability**

Challenges:
- Consistency in presence of *failures*.
- Consistency in presence of *concurrency*.

---

# Read/Write registers

- A **register**  represents each memory location.
- A register contains only positive integers and is initialized to $0$.
- Registers have two *operations*:
    - $\text{read}()$: return the current value of the register.
    - $\text{write}(v)$: update the register to value $v$.
- An operation is *not instantaneous*:
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
- Operation  $o_1$ and  $o_2$ are *concurrent* if neither precedes the other.
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
    - Ask the leader for latest value.
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
    - Ask the leader for latest value.
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

---

# Correctness

XXX

---

# $(N, N)$ atomic registers

XXX

---

# Simulating message passing?

XXX equivalence

---

# Summary

---

# References
