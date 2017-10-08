class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 3: Reliable broadcast

---

# Today

---

# Unreliable broadcast

.center.width-100[![](figures/lec3/unreliable-broadcast.png)]

---

class: center, middle

# Reliable broadcast abstractions

---

# Reliable broadcast abstractions

- *Best-effort broadcast*
    - Guarantees reliability only if sender is correct.
- *Reliable broadcast*
    - Guarantees reliability independent of whether sender is correct.
- *Uniform reliable broadcast*
    - Also considers the behavior of failed nodes.
- *Causal reliable broadcast*
    - Reliable broadcast with causal delivery order.

---

# Best-effort broadcast

.center[![](figures/lec3/beb-interface.png)]

---

# BEB example (1)

.center.width-100[![](figures/lec3/beb-example1.png)]

<span class="Q">[Q]</span> Is this allowed?

???

Not allowed.

---

# BEB example (2)

.center.width-100[![](figures/lec3/beb-example2.png)]

<span class="Q">[Q]</span> Is this allowed?

???

Allowed.

---

# Reliable broadcast

- Best-effort broadcast gives no guarantees if *sender crashes*.
- **Reliable broadcast**:
    - Same as best-effort broadcast +
    - If sender crashes, ensure *all or none* of the correct node deliver the message.

---

# Reliable broadcast

.center[![](figures/lec3/rb-interface.png)]

<span class="Q">[Q]</span> Can we weaken the definition of *Validity* while preserving the interface?

???

Validity: if correct $p$ broadcasts $m$, then $p$ itself eventually delivers $m$.

---

# RB example (1)

.center.width-100[![](figures/lec3/rb-example1.png)]

<span class="Q">[Q]</span> Is this allowed?

???

Allowed.

---

# RB example (2)

.center.width-100[![](figures/lec3/rb-example2.png)]

<span class="Q">[Q]</span> Is this allowed?

???

Allowed.

---

# RB example (3)

.center.width-100[![](figures/lec3/rb-example3.png)]

<span class="Q">[Q]</span> Is this allowed?

???

Not allowed.

---

# RB example (4)

.center.width-100[![](figures/lec3/rb-example4.png)]

<span class="Q">[Q]</span> Is this allowed?

???

Allowed.

---

# Uniform reliable broadcast

- Assume the broadcast enforces
    - Printing a message on paper
    - Withdrawing money from account in variable
- Assume sender broadcasts a message
    - Sender fails
    - No correct node delivers the message
    - Failed nodes deliver the message, is this OK?
- **Uniform** reliable broadcast ensures that if a message is delivered (by a correct or faulty process), then all correct processes deliver.

---

# Uniform reliable broadcast

.center[![](figures/lec3/urb-interface.png)]

---

class: center, middle

# Implementations

---

# Basic broadcast

.center[![](figures/lec3/beb-impl.png)]

Correctness:
- *BEB1. Validity*
    - If sender does not crash, every other correct node receives message by perfect channels.
- *BEB2+3. No duplication + no creation*
    - Guaranteed by perfect channels.

---

# Lazy reliable broadcast

- Assume a *fail-stop* distributed system model.
    - i.e., require a perfect failure detector.
- To broadcast $m$:
    - best-effort broadcast $m$
    - Upon `bebDeliver`:
        - Save message
        - `rbDeliver` the message
- If sender $s$ crashes, detect and really messages from $s$ to all.
    - case 1: get $m$ from $s$, detect crash of $s$, redistribute $m$
    - case 2: detect crash of $s$, get $m$ from $s$, redistribute $m$.
- Filter duplicate messages.

---

# Lazy reliable broadcast

.center[![](figures/lec3/lrb-impl.png)]

---

# LRB example (1)

.center.width-100[![](figures/lec3/lrb-case2.png)]

<span class="Q">[Q]</span> Which case?

???

Case 2

---

# LRB example (2)

.center.width-100[![](figures/lec3/lrb-case1.png)]

<span class="Q">[Q]</span> Which case?

???

Case 1

---

# Correctness of LRB

Correctness:
- *RB1-RB3*
    - Satisfied with best-effort broadcast.
- *RB4. Agreement*
    - When correct $p_j$ delivers $m$ broadcast by $p_i$
        - if $p_i$ is correct, BEB ensures correct delivery
        - if $p_i$ crashes,
            - $p_j$ detects this (because of completeness of the PFD)
            - $p_j$ uses BEB to ensure (BEB1) every correct node gets $m$.

---

# Eager reliable broadcast

- What happens if we use instead an *eventually* perfect failure detector?
    - Only affects performance, not correctness.
- Can we modify Lazy RB to not use a perfect failure detector?
    - Assume all nodes have failed.
    - Best-effort broadcast all received messages.

---

# Eager reliable broadcast

.center[![](figures/lec3/erb-impl.png)]

<span class="Q">[Q]</span> Show that eager reliable broadcast is correct.

---

# Uniformity

Neither Lazy RB nor Eager RB ensure *uniform* agreement.
- E.g., sender $p$ immediately RB delivers and crashes. Only $p$ delivered the message.

## Strategy for uniform agreement
- Before delivering a message, we need to ensure all correct nodes have received it.
- Messages are  **pending** until all correct nodes get it.
    - Collect acknowledgements from nodes that got the message.
- Deliver once all correct nodes acked.

---

# All-ack uniform reliable broadcast

.center.width-50[![](figures/lec3/aaurb-impl.png)]

---

# All-ack URB example

.center.width-100[![](figures/lec3/urb-example.png)]

---

class: smaller

# Correctness of All-ack URB

## Lemma
If a correct node $p$ BEB delivers $m$, then $p$ eventually URB delivers $m$.

Proof:
- A correct node $p$ BEB broadcasts $m$ as soon as it gets $m$.
- By BEB1, every correct node gets $m$ and BEB broadcasts $m$.
- Therefore $p$ BEB delivers from every correct node by BEB1.
- By completeness of the perfect failure detector, $p$ will not wait for dead nodes forever.
    - `canDeliver` becomes true and $p$ URB delivers $m$.

---

class: smaller

# Correctness of All-ack URB

- *URB1. Validity*
    - If sender is correct, it will BEB delivers $m$ by validity (BEB1)
    - By the lemma, it will therefore eventually URB delivers $m$.
- *URB2. No duplication*
    - Guaranteed because of the `delivered` set.
- *URB3. No creation*
    - Ensured from best-effort broadcast.
- *URB4. Uniform agreement*
    - Assume some node (possibly failed) URB delivers $m$.
        - Then `canDeliver` was true, and by accuracy of the failure detector, every correct node has BEB delivered $m$.
    - By the lemma, each of the nodes that BEB delivered $m$ will URB deliver $m$.

---

# URB for fail-silent

- All-ack URB requires a perfect failure detector (fail-stop).
- Can we implement URB in *fail-silent*,  without a perfect failure detector?
- **Yes**, provided a majority of nodes are correct.

.center[![](figures/lec3/maurb-impl.png)]

<span class="Q">[Q]</span> Show that this variant is correct.

---

class: center, middle

# Probabilistic broadcast

---

# Scalability of reliable broadcast

- In order to broadcast a message, the sender needs
    - to send messages to all other processes,
    - to collect some form of acknowledgement.
    - $O(N^2)$ are exchanged in total.
        - If $N$ is large, this can become overwhelming for the system.  
- Bandwidth, memory or processing resources may limit the number of messages/acknowledgements that may be sent/collected.
- Hierarchical schemes reduce the total number of messages.
    - This reduces the load of each process.
    - But increases the latency and fragility in case of failures.

.center.width-100[![](figures/lec3/comm-acks.png)]

---

# Epidemic dissemination

- **Epidemiology** studies the spread of a disease or infection in terms of populations of infected/uninfected individuals and their rates of change.
- Nodes infect each other through messages sent in **rounds**.
    - The *fanout* $k$ determines the number of messages sent by each node.
    - The *number of rounds* is limited to $R$.
- Total *number of messages* is usually less than $O(N^2)$.
- No node is overloaded.

.center[![](figures/lec3/pb-rounds.png)]

---

# Probabilistic broadcast

.center[![](figures/lec3/pb-interface.png)]
---

# Eager probabilistic broadcast

.center[![](figures/lec3/epb-impl.png)]

---

# The mathematics of epidemics


---

# Lazy Probabilistic broadcast

- Eager probabilistic broadcast consumes **considerable resources** and causes many **redundant transmissions**.
    - When too many nodes are infected, the rate of newly infected node decreases.
- Assume *a stream of messages* to be broadcast.
- Broadcast messages in two phases:
    - *Phase 1 (data dissemination)*: run probabilistic broadcast with a large probability $\epsilon$ that reliable delivery fails. That is, assume a constant fraction of nodes obtain the message (e.g., $\frac{1}{2}$).
    - *Phase 2 (recovery)*: upon delivery, detect omissions through sequence numbers and initiate retransmissions with gossip.

---

class: smaller

# Lazy Probabilistic broadcast

## Phase 1: data dissemination

.center.width-70[![](figures/lec3/lpb-impl1.png)]

---

class: smaller

# Lazy Probabilistic broadcast

## Phase 2: recovery

.center.width-70[![](figures/lec3/lpb-impl2.png)]

---

class: center, middle

# Causal reliable broadcast

---

# Motivation

---

# Causal broadcast

---

# No-waiting causal broadcast

---

# Waiting causal broadcast

---

# Summary

---

# References

- Eugster, Patrick T., et al. "Epidemic information dissemination in distributed systems." Computer 37.5 (2004): 60-67.
