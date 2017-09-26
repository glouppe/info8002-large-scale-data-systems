class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 2: Basic abstractions

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
def on_eventA(event):   # handler for events of type A
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
- Layers of distributed programming abstractions are typically in the middle.

---

# Automata and steps


---

# Liveness and safety

---

# Abstracting processes

???

2.2
Failures

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
