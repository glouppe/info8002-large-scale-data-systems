class: middle, center, title-slide

# Large-scale Distributed Systems

Lecture 1: Distributed systems

---

class: middle, center

# Introduction to distributed systems

---

# Operating systems

Can you name examples of *operating systems*?

--

- Android
- Chrome OS
- FreeBSD
- iOS
- macOS
- OS/2
- RISC OS
- Solaris
- Windows
- ...

---

# Operating systems

What is an *operating system*?

## Definition

The low-level software which handles the interface to peripheral hardware,
schedules tasks, allocates storage, and presents a default interface to the user
when no application program is running.

---

# Distributed systems

Can you name examples of *distributed systems*?

--

- The web
- Wireless networks
- Telephone networks
- DNS
- Massively multiplayer online games
- Distributed databases
- BitTorrent (peer-to-peer overlays)
- A cloud, e.g. Amazon EC2/S3, Microsoft Azure
- A data center, e.g. a Google data center, AWS
- The bitcoin network

---

# Distributed systems

What is a *distributed system*?

## Definition

A distributed system is a collection of entitites with a common goal, each of
which is *autonomous*, *programmable*, *asynchronous* and *failure-prone*, and
which communicate through an **unreliable** communication mediu.

---

# Why is it difficult to build?

- **Scale**: hundreds or thousands of machine
    - Google: 4k-machine MapReduce cluster
    - Yahoo!: 4k-machine Hadoop cluster
    - Akamai: 70k machines, distributed over the world
    - Facebook: 60k machines providing the service
    - Hard enough to program one machine!
- **Dynamism**: machines do fail!
    - 50 machine failures out of 20k machine cluster per day (reported by Yahoo!)
    - 1 disk failure out of 16k disks every 6 hours (reported by Google)
- Additional constraints: *concurrent execution*, *consistency*, etc.

---

# Theme 1: Communications

- *How do you talk to another machine?*
    - Networking basics
- *How do you talk to multiple machines at once?*
    - Multicast, Gossiping.

---

# Theme 2: Consensus

- *How do multiple machines reach an agreement?*
    - Time and synchronization, global states, mutual exclusion, leader election, paxos.
- **Bad news**: it is impossible!
    - The impossibility of consensus.

---

# Theme 3: Concurrency

- *How do you control access to shared resources?*
    - Distributed mutual exclusion, distributed transactions, 2/3-phase commit, etc.

---

# Theme 4: Failures

- *How do you know if machine has failed?*
    - Failure detection.
- *How you do program your system to operate continually even under failure?*
    - Gossiping, replication.

---

# Distributed computing systems

---

# Distributed storage systems

---

class: middle, center

# Networking basics

---

class: middle, center

# Overview of distributed systems

---

# Summary

---

# References
