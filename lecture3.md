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

# Implementing BEB

---

# Lazy reliable broadcast

---

# Eager reliable broadcast

---

# Uniform eager RB

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

class: center, middle

# Randomized broadcast

---

# Scalability of reliable broadcast

---

# Epidemic dissemination

---

# Probabilistic broadcast

---

# Eager probabilistic broadcast

---

# Lazy Probabilistic broadcast

---

# Summary

---

# References
