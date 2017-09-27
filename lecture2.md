class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 2: Basic abstractions

---

# Outline

- In this lesson, we will define **basic abstractions** that capture the
  fundamental characteristics of various distributed systems, and on top of
  which we will later define more elaborate abstractions.
- Three main abstractions:
    - *Process* abstractions
    - *Link* abstractions
    - *Timing* abstractions
- A *distributed system model* = a combination of the three categories of abstractions.

---

# Need for distributed abstractions

- Core of any distributed system is a set of distributed algorithms.
    - Implemented as a middleware between network (OS) and the application.
- **Reliable** applications need underlying services **stronger** than transport protocols (e.g., TCP or UDP).

.center[![](figures/lec2/middleware.png)]

---

# Network protocols are not enough

.pull-right[![Distributed abstractions](figures/lec2/abstractions.png)]

- Communication
    - Reliability guarantees (e.g. with TCP) are only offered for **one-to-one** communication (client-server).
    - How to do *group communication*?
- High-level services
    - Sometimes one-to-many communication is not enough.
    - Need *reliable high-level services*.

---

class: middle, center

# Distributed computation

---

# Distributed computation

.center[![](figures/lec2/dp-abstraction.png)]

- A *distributed algorithm* is a distributed collection of $N$ processes implemented by *identical* automata.
- The automaton at a process regulates the way the process executes its computation steps.
- Processes jointly implement the application.
    - Need for **coordination**.
---

# Programming with events

- Every process consists of **modules** or **components**.
    - Modules may exist in multiple instances.
    - Every instance has a unique identifier and is characterized by a set of properties.
- Asynchronous **events** represent *communication* or *control flow* between components.
    - Each component is constructed as a state-machine whose transitions are triggered by the reception of events.
    - Events carry information (sender, message, etc)
- Reactive programming model:
.center[![](figures/lec2/handler-notations.png)]
- Effectively, a distributed algorithm is described by a set of event handlers.

---

# Layered modular architecture

.center[![](figures/lec2/layering.png)]

- Components can be composed locally to build software stacks.
    - The top of the stack is the *application layer*.
    - The bottom of the stack  the *transport* or *network* layer.
- Distributed programming abstraction layers are typically in the middle.
- We assume that every process executes the code triggered by events in a mutually exclusive way, without concurrently processing $\geq$ 2 events.

---

# Execution

.center[![](figures/lec2/step.png)]

- The **execution** of a distributed algorithm is a *sequence of steps* executed by its processes.
- A **process step** consists in
    - *receiving* a message from another process,
    - *executing* a local computation,
    - *sending* a message to some process.
- Local messages between components are treated as local computation.
- We assume *deterministic* process steps (with respect to the message received and the local state prior to executing a step).

---

# Liveness and safety

- Implementing a distributed programming abstraction requires satisfying its *correctness*
  in all possible executions of the algorithm.
    - i.e., in all possible interleaving of steps.
- Correctness of an abstraction is expressed in terms of **liveness** and **safety** properties.
    - *Safety*: properties that state that nothing bad ever happens.
        - A safety property is a property such that, whenever it is violated in some execution $E$ of an algorithm,
        there is a prefix $E'$ of $E$ such that the property will be violated in any extension of $E'$.
    - *Liveness*: properties that state something good eventually happens.
        - A liveness property is a property such that for any prefix $E'$ of $E$, there exists an extension of $E'$ for which
        the property is satisfied.
- Any property can be expressed as the conjunction of safety property and a liveness property.

---

# Correctness example (1)

.grid[
.col-2-3[
## Traffic lights at an intersection
- Safety: only one direction should have a green light.
- Liveness: every direction should eventually get a green light.
]
.col-1-3[
![](figures/lec2/lights.jpg)
]
]

---

# Correctness example (2)

## TCP
- Safety: messages are not duplicated and received in the order they were sent.
- Liveness: messages are not lost.

---

# Assumptions

- In our abstraction of a distributed system, we need to specify the *assumptions* needed for the algorithm to be **correct**.

- A distributed system model includes assumptions on:
    - **failure** behavior of processes and channels
    - **timing** behavior of processes and channels


---

class: middle, center

# Process abstractions

---

# Process failures

- Processes may **fail** in four different ways:
    - *Crash-stop*
    - *Omissions*
    - *Crash-recovery*
    - *Byzantine / arbitrary*

- Processes that do not fail in an execution are **correct**.

---

# Crash-stop failures

- A process stops taking steps.
    - Not sending messages.
    - Not receiving messages.
- **By default**, we assume the crash-stop process abstraction.
    - Hence, do not recover.
    - Q: Does this mean that processes are not allowed to recover?

---

# Omission failures

- Process omits sending or receiving messages.
    - *Send omission*: A process omits to send a message it has to send according to its algorithm.
    - *Receive omission*: A process fails to receive a message that was sent to it.
- In general, omission failures are due to buffer overflows.
- With omission failures, a process deviates from is algorithm by dropping messages that should have been exchanged with other processes.

---

# Crash-recovery failures

- A process might crash.
    - It stops taking steps, not receiving and sending messages.
- It may **recover** after crashing.
    - The process emits a `<Recovery>` event upon recovery.
- Access to **stable storage**:
    - May read/write (*expensive*) to permanent storage device.
    - Storage survives crashes.
    - E.g., save state to storage, crash, recover, read saved state, ...
- A failure is different in the crash-recovery abstraction:
    - A process is **faulty** in an execution if
        - It crashes and never recovers, or
        - It crashes and recovers infinitely often.

    - Hence, a **correct** process may crash and recover.

---

# Byzantine failures

- A process may behave arbitrarily.
    - Sending messages not specified by its algorithm.
    - Updating its state as not specified by its algorithm.

- Might behave **maliciously**, attacking the system.
    - Several malicious nodes might collude.

---

# Fault-tolerance hierarchy

.center[![](figures/lec2/failures.png)]

Q: Explain how failure modes are special cases of one another.

---

class: middle, center

# Communication abstractions

---

# Links

- In our abstraction, every process may **logically** communicate with every other process (a).
- The physical implementation may differ (b-d).

.stretch[![](figures/lec2/links.png)]

---

# Link failures

- *Fair-loss links*
    - Channel delivers any message sent, with non-zero probability.

- *Stubborn links*
    - Channel delivers any message sent infinitely many times.
    - Can be implemented using fair-loss links.

- *Perfect links* (i.e. reliable)
    - Channel delivers any message sent exactly once.
    - Can be implemented using stubborn links.
    - **By default**, we assume the perfect links abstraction.

- Q: What abstraction do UDP and TCP implement?

---

# Perfect links: interface

.center[![](figures/lec2/pl-interface.png)]

Q: Which property is safety/liveness/neither?

---

# Perfect links: implementation

.center[![](figures/lec2/pl-impl.png)]

- Q: Does this implementation ensure correctness?
- Q: How does TCP efficiently maintain its `delivered` log?


---

class: middle, center

# Timing assumptions

---

---

class: middle, center

# Timing abstractions

---

???
- Timing assumptions (2.4)
- Failure detection (2.5)
- Leader election (2.5)
- Relations between FD and LE

---

class: middle, center

# Distributed system models

---

???

2.6

---

# Summary

---

# References
