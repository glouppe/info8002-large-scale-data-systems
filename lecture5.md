class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 5: Consensus

---

# Today

---

# Consensus

- **Consensus** is the problem of making processes all *agree* on one of the values they propose.
- Solving consensus is **key** to solving many problems in distributed computing:
    - synchronizing replicated state machines;
    - electing a leader;
    - managing group membership;
    - deciding to commit or abort distributed transactions.
- Any algorithm that helps multiple processes *maintain common state* or to *decide on a future action*, in a model where processes may fail, *involves solving a consensus problem*.

---

# Consensus

.center.width-100[![](figures/lec5/consensus-interface.png)]

<span class="Q">[Q]</span> Which is safety, which is liveness?

???

- Termination: liveness
- Validity: safety
- Integrity: safety
- Agreement: safety

---

# Sample execution

.center.width-100[![](figures/lec5/consensus-exec.png)]

<span class="Q">[Q]</span> Does this satisfy consensus?

???

Yes

---

# Uniform consensus

.center[![](figures/lec5/uniform-consensus-interface.png)]

---

# Sample execution

.center.width-100[![](figures/lec5/consensus-exec.png)]

<span class="Q">[Q]</span> Does this satisfy uniform consensus?

???

No

---

class: center, middle

.width-100[![](figures/lec5/impossibility.png)]

---

# Impossibility of consensus

So, are we done? **No!**
- The FLP impossibility result holds for *asynchronous systems* only.
- Consensus can be implemented in **synchronous** and **partially synchronous** systems.
- *Paxos*: consensus algorithm in asynchronous systems for which termination is not guaranteed, but where validity, integrity and agreement are guaranteed.

---

class: center, middle

# Consensus in fail-stop

---

class: smaller

# Hierarchical consensus

- Assume a **perfect failure detector** (synchronous system).
- Assume processes $1, ..., N$ form an ordered **hierarchy** as given by a $\text{rank}(p)$ function.
    - $\text{rank}(p)$ is a *unique* number between $1$ and $N$ (e.g., the pid).
- Hierarchical consensus ensures that *the correct process with the lowest rank imposes its value* on all the other processes.
    - If $p$ is correct and rank $1$, it imposes its values on all other processes by broadcasting its proposal.
    - If $p$ crashes immediately and $q$ is correct and rank 2, then it ensures that $q$'s proposal is decided.
    - The core of the algorithm addresses the case where $p$ is faulty but crashes after sending some of its proposal messages and $q$ is correct.
- Hierarchical consensus works *in rounds*, with a rotating *leader*.
    - At round $i$, process $p$ with rank $i$ is the leader. It decides its proposal and broadcasts it to all processes.
    - All other processes that reach round $i$ wait before taking any actions, until they deliver this message or until they detect the crash of $p$.

---

# Hierarchical consensus

.center.width-60[![](figures/lec5/hierarchical-consensus.png)]

---

# Execution without failure

.center.width-100[![](figures/lec5/hierarchical-consensus-exec1.png)]

---

# Execution with failure (1)

.center.width-100[![](figures/lec5/hierarchical-consensus-exec2.png)]

<span class="Q">[Q]</span> Uniform consensus?

<span class="Q">[Q]</span> How many failures can be tolerated?

???

- Not uniform consensus.
- $N-1$ failures at most.

---

# Execution with failure (2)

.center.width-100[![](figures/lec5/hierarchical-consensus-exec3.png)]

---

# Correctness

- *Termination*: Every correct process eventually decides some value.
    - Every correct node makes it to the round it is leader in.
        - If some leader fails, completeness of the FD ensures progress.
        - If leader correct, validity of BEB ensures delivery.
- *Validity*: If a process decides $v$, then $v$ was proposed by some process.
    - Always decide own proposal or adopted value.
- *Integrity*: No process decides twice.
    - Rounds increase monotonically.
    - A node only decides once in the round it is leader.
- *Agreement*: No two correct processes decide differently.
    - Take correct leader with minimum rank $i$.
        - By termination, it will decide $v$.
        - It will BEB $v$:
            - Every correct node gets $v$ and adopts it.
            - No older proposals can override the adoption.
            - All future proposals ans decides will be $v$

---

# Hierarchical uniform consensus

- Same as *Hierarchical consensus*
- A round consists of *two communication steps*:
    - The leader BEB broadcasts its proposal
    - The leader collects acknowledgements
- Upon reception of all acknowledgements, **RB** broadcast the decision.
    - This ensures that if a decision is made (at a faulty or correct process), then this decision will be made at all correct processes.

---

# Hierarchical uniform consensus

.center.width-60[![](figures/lec5/uniform-hierarchical-consensus1.png)]

---

.center.width-60[![](figures/lec5/uniform-hierarchical-consensus2.png)]

---

class: middle, center

# Consensus in fail-noisy

---

# Consensus in partially synchronous systems

- Hierarchical consensus requires a *perfect failure detector*. Can we switch to an *eventually perfect failure detector* (i.e.,  **fail-noisy**)?
- A *false suspicion* (i.e., a violation of strong accuracy) might lead to the **violation of agreement**.
    - If a process is suspected while it is actually correct, then two processes might decide differently.
- *Not suspecting* a crashed process (i.e., a violation of strong completeness) might lead to the **violation of termination**.

.center.width-100[![](figures/lec5/hierarchical-consensus-false.png)]

---

# Towards consensus...

We will build a consensus component in *fail-noisy* by combining three abstractions:

- an eventual leader detector
- an epoch-change abstraction
- an epoch consensus

---

# Eventual leader detector

.center[![](figures/lec5/ele.png)]

<span class="Q">[Q]</span> This abstraction can be implemented from an *eventually perfect failure detector*. How?

---

# Epoch-Change

- When a leader is chosen, the **Epoch-Change** abstraction signals the start of a new epoch by triggering a StartEpoch event.
    - The event contains:
        - an epoch timestamp $ts$
        - a leader process $l$.
- We require *monotonicity* of the timestamps for the epochs started at one correct process.
- We require the *same leader* for every correct process at a given timestamp.
- **Eventually**, the component ceases to start new epochs. The last epoch started at every correct process must the same and the leader is correct.

---

# Epoch-Change

.center[![](figures/lec5/ec-interface.png)]

---

# Leader-based Epoch-Change

- Every process $p$ maintains *two timestamps*:
    - a timestamp $lastts$ of the last epoch that is has started;
    - a timestamp $ts$ of the last epoch it attempted to start as a leader.
- When the leader detector makes $p$ trust itself, $p$ adds $N$ to $ts$ and broadcasts a NewEpoch message with $ts$.
- When $p$ receives a NewEpoch message with parameter $newts > lastts$ from $l$ and $p$ most recently trusted $l$, then $p$ triggers a StartEpoch message.
- Otherwise, $p$ informs the aspiring leader $l$ with a NACK that a new epoch could not be started.
- When $l$ receives a NACK and still trusts itself, it increments $ts$ by $N$ and tries again to start a new epoch.

---

# Leader-based Epoch-Change

.center.width-60[![](figures/lec5/ec-impl.png)]

---

# Sample execution (1)

.center.width-100[![](figures/lec5/ec-exec1.png)]

---

# Sample execution (2)

.center.width-100[![](figures/lec5/ec-exec2.png)]

---

# Epoch Consensus

.center[![](figures/lec5/econs-interface1.png)]

---

.center[![](figures/lec5/econs-interface2.png)]

---

# Read/Write Epoch Consensus

.center[![](figures/lec5/rwec-impl1.png)]

---

.center[![](figures/lec5/rwec-impl2.png)]

---

# Leader-Driven Consensus

.center.width-60[![](figures/lec5/ld-consensus.png)]

---

class: middle, center

# Total order broadcast

---

# Total order broadcast

???

== atomic broadcast

---

# Replicated state machines

---

class: middle, center

# Consensus in asynchronous systems

---

# Paxos

---

# Summary

---

# References

- Fischer, Michael J., Nancy A. Lynch, and Michael S. Paterson. "Impossibility of distributed consensus with one faulty process." Journal of the ACM (JACM) 32.2 (1985): 374-382.
