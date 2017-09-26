class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 2: Basic abstractions

---

In this lesson, ...

XXX

---

# Programming abstractions

- *Sequential programming*
    - Array, record, list, ...  

- *Concurrent programming*
    - Thread, semaphore, monitor, ...

- *Distributed programming*
    - Reliable broadcast
    - Shared memory
    - Consensus
    - Atomic commit
    - ...

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
- Asynchronous **events** represent *communication* or *control flow* between component.
    - Each component is constructed as a state-machine whose transitions are triggered by the reception of events.
    - Events may carry information (e.g., data message, group information)
- Reactive programming model:

```python
def upon_eventA(event):   # handler for events of type A
    # do something
    # ...
    trigger(eventB(...))
```

- In our abstraction, a distributed algorithm is effectively described by a set of event handlers.

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

- Correctness of an abstraction is expressed in terms of **liveness** and **safety**.
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

# Model/Assumptions

In our abstraction of a distributed system, we need to specify the *assumptions* needed for the algorithm to be **correct**.

We need assumptions on:
- **failure** behavior of processes and channels
- **timing** behavior of processes and channels.

---

# Process failures

- Processes may **fail** in four different ways:
    - *Crash-stop*
    - *Omissions*
    - *Crash-recovery*
    - *Byzantine / arbitrary*

- Processes that do not fail in an execution are **correct**.

.center[![](figures/lec2/failures.png)]
.caption[Failure modes of a process]

---

# Crash-stop failures

---

# Omission failures

---

# Crash-recovery failures

---

# Byzantine failures

---

# Abstracting communication

???

2.3

---

# Abstracting time

???
- Timing assumptions (2.4)
- Failure detection (2.5)
- Leader election (2.5)
- Relations between FD and LE

---

# Distributed abstractions

???

@.6

---

# Summary

---

# References
