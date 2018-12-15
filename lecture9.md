class: middle, center, title-slide

# Large-Scale Data Systems

Lecture 9: Distributed Hash Tables

<br><br>
Prof. Gilles Louppe<br>
[g.louppe@uliege.be](g.louppe@uliege.be)

---

# Today

How to design a large-scale distributed system similar to a hash table?

- Chord
- Kademlia

---

class: middle, center, black-slide

.width-80[![](figures/lec9/iceberg.png)]

---

# Hash tables

A **hash table** is data data structure that implements an associative array abstract data type, i.e. a structure than can map keys to values.
- It uses a *hash function* to compute an index into array of buckets or slots, from which the desired value can be found.
- Efficient and scalable: $\mathcal{O}(1)$ look-up and store operations (on a single machine).

.center.width-60[![](figures/lec9/hash-table.svg)]

---

# Distributed Hash Tables

A **distributed hash table** (DHT) is a class of decentralized distributed systems that provide a lookup service similar to a hash table.
- Extends upon multiple machines in the case when the data is so large we cannot store it on a single machine.
- Robust to *faults*.

---

class: middle

## Interface

- $\text{put}(k, v)$
- $\text{get}(k)$

## Properties

- When $\text{put}(k, v)$ is completed, $k$ and $v$ are reliably stored on the DHT.
- If $k$ is stored on the DHT, a process will eventually find a node which stores $k$.

---

class: middle

# Chord

---

# Chord

Chord is a protocol and algorithm for a peer-to-peer distributed hash table.
- It organizes the participating nodes in an overlay network, where each node is responsible for a set of keys.
- Keys are defined as $m$-bit identifiers, where $m$ is a predefined system parameter.
- The overlay network is arranged in a **identifier circle** ranging from $0$ to $2^m - 1$.
    - A *node identifier* is chosen by hashing the IP address.
    - A *key identifier* is chosen by hashing the key.
- Based on **consistent hashing** with SHA-1 hash function.
- Supports a single operation: $\text{lookup}(k)$.
    - Returns the host which holds the data associated with the key.

---

# Consistent hashing

## Traditional hashing

- Set of $n$ bins.
- Key $k$ is assigned to a particular bin.
- If $n$ changes, all items need to be rehashed.
    - E.g. when `bin_id = hash(key) % num_bins`.

## Consistent hashing

- Evenly distributes $x$ objects over $n$ bins.
- When $n$ changes:
  - Only $\mathcal{O}(\frac{x}{n})$ objects need to be rehashed.
  - Uses a deterministic hash function.

---

class:  middle

Consistent hashing in Chord assigns keys to nodes as follows:

- Key $k$ is assigned to the first node whose identifier is equal to or follows $k$ in the identifier space.
    - i.e., the first node on the identifier ring starting from $k$.
- This node is called the *successor node* of $k$, denoted $\text{successor}(k)$.
- Enable **minimal disruption**.

---

class: middle

To maintain the consistent (hashing) mapping, let us consider a node $n$ which
- joins: keys assigned to $\text{successor}(n)$ are now assigned to $n$. Which? $\text{predecessor}(n) < k \leq n$
- leaves: All of $n$'s assigned keys are assigned to $\text{successor}(n)$.

.center.width-80[![](figures/lec9/dht-chord.png)]

---

# Routing

The core usage of the Chord protocol is to query a key from a client (generally a node as well), i.e. to find $\text{successor}(k)$.

## Basic query

- Any node $n$ stores its immediate successor $\text{successor}(n)$.
- If the key cannot be found locally, then the query is passed to the node's successor.
- Scalable yes, but $\mathcal{O}(n)$ operations are required.
    - **Unacceptable** in  large systems!

---

class: middle

## Finger Table

- As before, let $m$ be the number of bits in the identifier.
- Every node $n$ maintains a routing (finger) table with at most $m$ entries.
- Entry $i$ in the finger table of node $n$:
  - First node $s$ that succeeds $n$ by at least $2^{i - 1}$ on the identifier circle.
  - Therefore, $s = \text{successor}((n + 2^{i-1})\mod 2^m)$

---

class: middle

## Finger table example

- $m = 4$ bits $\rightarrow$ max 4 entries in the routing table.
- $i$-th entry in finger table: $s = \text{successor}((n + 2^{i - 1})\text{~}\mathrm{mod}\text{~}2^m)$
.center.width-50[![](figures/lec9/chord-clean.png)]

---

class: middle

## First entry

- $n=4$, $i = 1$
- $s = \text{successor}((n + 2^{i-1}) \text{~}\mathrm{mod}\text{~}2^m) = \text{successor}(5) = 5$

.center.width-80[![](figures/lec9/chord-finger-1.png)]

---

class: middle

## Second entry

- $n=4$, $i = 2$
- $s = \text{successor}((n + 2^{i-1}) \text{~}\mathrm{mod}\text{~}2^m) = \text{successor}(6) = 8$

.center.width-80[![](figures/lec9/chord-finger-2.png)]

---

class: middle

## Third entry

- $n=4$, $i = 3$
- $s = \text{successor}((n + 2^{i-1}) \text{~}\mathrm{mod}\text{~}2^m) = \text{successor}(8) = 8$

.center.width-80[![](figures/lec9/chord-finger-3.png)]

---

class: middle

## Fourth entry

- $n=4$, $i = 4$
- $s = \text{successor}((n + 2^{i-1}) \text{~}\mathrm{mod}\text{~}2^m) = \text{successor}(12) = 14$

.center.width-80[![](figures/lec9/chord-finger-4.png)]

---

class: middle

## Properties of the finger table

- Every nodes stores only a small number of other nodes.
- Every nodes knows more about *close* nodes compared to far away nodes.

What happens when a node $n$ does not know the successor of a key $k$ (probably since nodes can join and leave arbitrarily)?
- *Intuition*: If $n$ can find a node whose ID is closer to $k$ than its own, find that node, until it finds the successor of $k$.
    - Jump to the *closest predecessor* node of the desired identifier (with high probability it knows more about the desired identifier).
- **Invariant required**: Every node's successor is correctly maintained.

---

class: middle

## Lookup

```
n.find_successor(id)
  if (id ∈ (n, successor])
    return successor;
  else
    // forward the query around the circle
    n0 = successor.closest_preceding_node(id);
    return n0.find_successor(id);
```

```
n.closest_preceding_node(id)
  for i = m downto 1
    if (finger[i]∈(n,id))
      return finger[i];
  return n;
```

---

class: middle

## Example: finding $\text{successor}(k=3)$ from $n=4$

1. $n=4$ checks if $k$ is in the interval (4, 5].
2. It not, $n=4$ checks its  finger table (starting from the last entry, i.e., $i = m$).
   1. Is *node 14* in the interval (4, 4)? *Yes!*
3. $n=14$ checks if $k$ is in the interval (14, 0].
4. No, $n=14$ checks its finger table for closest preceding node.
   1. Return *node 0*.
5. $n=0$ checks if $k$ is in the interval (0, 4]. *Yes!*

$\rightarrow$ Node 0 is the preceding node of $k = 4$. Therefore $\text{successor}(k=3)=4$.

Of course, one could implement a mechanism that prevents node 4 from looking up its own preceding node in the network.

---

# Join

What needs to happen in order to ensure a consistent network when a node $n$ joins the network by connecting to a node $n^\prime$?

1. Initialize the predecessor and fingers of node $n$.
2. Update the fingers and predecessors of existing nodes to reflect the addition of $n$.
3. Transfer the keys and their corresponding values to $n$.

---

class: middle

## Initializing fingers and predecessor

- $n$ learns its predecessor and fingers by asking $n^\prime$ to look them up $\text{find-predecessor}(n)$.
- Finger table can also constructed through this mechanism.
  - Remember: $i$-th entry is $\text{successor}((n + 2^{i - 1})\text{~}\mathrm{mod}\text{~}2^m)$
  - However: $\mathcal{O}(m \text{~log~} N)$ look-ups, can we do better?
  - Check if the $i$-th finger is also correct for $i + 1$.
  - Happens when there is no node in that interval, meaning, `finger[i].node >= finger[i + 1].start`.
  - This change allows a new node to complete its finger table with "high probability" in $\mathcal{O}(\text{log~}N)$ steps.

---

class: middle

## Updating fingers of existing nodes

- Node $n$ will become the $i$-th finger of a node $p$ if and only if:
  - $p$ precedes $n$ by at least $2^{i - 1}$.
  - The $i$-th finger of node $p$ succeeds $n$.
- The first node that can meet these two conditions is the immediate predecessor of $n$, which is $n - 2^{i -1}$.
- Then it increments $i$ and finds the next predecessor which meets this criterion (thus moving counter-clockwise).

---

class: middle

## Transferring keys

- $n$ can become the successor only for keys that were previously the responsibility of the node immediately following $n$.
- $n$ only needs to contact the successor of $n + 1$ to transfer responsibility of all relevant keys.

---

# Fault-tolerance

## Failures

A failure of $n$ must not be allowed to disrupt queries.
- Maintain a list of possible successors.
- A different thread maintains the finger table (and notifies others) in parallel.

## Replication

- Use the same successor-list to replicate the data!

---

# Summary

- Fast lookup $\text{log}(N)$
- Small routing table $\text{log}(N)$
- Handling failures and addressing replication (load balance) using same mechanism (successor list).
- Relatively small join/leave cost.
- Iterative lookup process.
- Timeouts to detect failures.
- No guarantees (with high probability ...).
- Routing tables must be correct.

---

class: middle

# Kademlia

---

# Kademlia

- Configuration information spreads automatically as a side-effect of key look-ups (gossiping).
- Nodes have enough knowledge and flexibility to route queries through low-latency paths.
- Asynchronous queries to avoid timeout delays from failed nodes.
- Minimizes the number of configuration messages (guarantee).
- 160-bit identifiers (e.g., using SHA-1 or some other hash function, implementation specific).
- Key-Value pairs are stored on nodes based on *closeness* in the identifier space.
- Identifier based *routing* algorithm by imposing a *hierarchy* (virtual overlay network).

---

# System description

- $m = 160$ bits
- Treat nodes as leaves in an (unbalanced) binary tree (sorted by prefix)
- The Kademlia protocol ensures that every node knows at least one other node in every sub-tree.
  - Guarantees that any node can locate any other node given its identifier.

.center.width-70[![](figures/lec9/kademlia-subtrees.png)]

---

class: middle

## Node distance

Before we look into storing and retrieving key value pairs in Kademlia, we first define a notion of *identifier closeness*.

- This allows us to store and retrieve information on $k$ (system parameter) closest nodes.
- The distance between two identifiers is defined as: $d(x, y) = x \oplus y$.

$\rightarrow$ Ensures redundancy

---

class: middle

## Node State

- For every prefix $0 < i < 160$, every node keeps a list of (IP address, Port, ID) for nodes of distance between $2^i$ and $2^{i+1}$: *k-buckets*.
- Every k-bucket is sorted by time last seen (descending, i.e, last-seen first).
- When a node receives a message, it updates the corresponding k-bucket for the sender's identifier. If the sender already exist, it is moved to the tail of the list.
  - **Important**: If the k-bucket is full, the node pings the **last** seen node and checks if it is still available. **Only if** the node is **not available** it will replace it.
  - Policy of replacement only when a nodes leaves the network $\rightarrow$ prevents Denial of Service (DoS) attacks (e.g., flushing routing tables).

---

class: middle

## k-bucket

.center.width-80[![k-bucket](figures/lec9/k-bucket.png)]

---

# Kademlia protocol

Provides 4 RPC's (Remote Procedure Call):

- `PING(id)` returns (IP, Port, ID)
  - Probes the node to check whether it is still online.
- `STORE(key, value)`
- `FIND_NODE(id)` returns (IP, Port, ID) for the $k$ nodes it knows about closest to ID.
- `FIND_VALUE(key)` returns (IP, Port, ID) for the $k$ nodes it knows about closest to ID.
  - **OR** the value if it maintains the key.

---

class: middle

## Node Lookup Procedure

The most important procedure a Kademlia participant must perform is locating the $k$ closest nodes to some given identifier.

- Kademlia achieves this by performing a recursive (more iterative) lookup procedure.
- The initiator issues asynchronous `FIND_NODE` requests to $\alpha$ (system parameter) nodes it has chosen.
  - Parallel search with the cost of increased network traffic.
  - Nodes return the $k$ closest nodes to the query ID.
  - Repeat and select the $\alpha$ nodes from the new set of nodes.
  - Terminate when set doesn't change.
  - **Possible optimization**: choose $\alpha$ nodes with lowest latency.

---

class: middle

## Storing data

Using the `FIND_NODE(id)` procedure, *storing* and making data *persistent* is trivial.

$\rightarrow$ Use $k$ closest node to store and persist the data.

- To ensure persistence in the presence of *node failures*, every node periodically republishes the key-value pair to the $k$ closest nodes.
- Updating scheme can be implemented. For example: delete data after 24 after publication to limit stale information.

---

class: middle

## Retrieving data

1. Find $k$ closest nodes of the specified identifier using `FIND_VALUE(id)`.
2. Halt procedure whenever the set of closest nodes doesn't change or a value is returned.

$\rightarrow$ For caching purposes, once a lookup succeeds, the requesting node stores the key-value pair at the *closest node to the key that did not return the value*.

- Because of the *unidirectionality* of the topology (requests will usually follow the same path), future searches for the same key are likely to hit cached entries before querying the closest node.

$\rightarrow$ Induces problem with popular nodes: *over-caching*.

**Solution**: Set expiration time *inversely proportional* to the distance between the true identifier and the current node identifier.

---

# Join

Very simple approach compared to other implementations.

1. Node $n$ initializes it's k-bucket (empty).
2. A node $n$ connects to an already participating node $j$.
3. Node $n$ then performs a *node-lookup* for its own identifier.
   - Yielding the $k$ closest node.
   - By doing so $n$ inserts itself in other nodes $k$-buckets.

**Note**: The new node should store keys which are the closest to its own identifier by obtaining the $k$-closest nodes.

---

# Leave and failures

Again, as is joining, leaving is very simple as well.

$\rightarrow$ Just disconnect.

- Failure handling is *implicit* in Kademlia due to *data persistence*.
- No special actions required by other nodes (failed node will just be removed from the k-bucket).

---

# Routing and Routing Table

- Routing table is an (unbalanced) binary tree whose leaves are $k$-buckets.
- Every $k$-bucket contains some nodes with a common prefix.
- The shared prefix is the $k$-buckets position in the binary tree.

$\rightarrow$ Thus, a $k$-buckets covers some range of the 160 bit identifier space.

- All $k$-buckets cover the *complete* identifier space with *no* overlap.

---

# Dynamic Construction of the Routing Table

- Nodes in the routing table are allocated dynamically as needed.
- A bucket is split whenever the $k$-bucket is *full* and the range *includes* the node's own *identifier*.

.center[
.width-80[
![k-bucket](figures/lec9/k-bucket.png)
]
]

---

# Example: Routing Table

- $k$ = 2
- $\alpha = 1$ (no asynchronous requests, also no asynchronous pings)
- Node identifier (000000) is *not* in the routing table

.center[
.width-80[
![Kademlia Routing 1](figures/lec9/kademlia-routing-1.svg)
]
]

---

class: middle, center

### Node `000111` is involved with an RPC request, what happens?

.center[
.width-100[
![Kademlia Routing 2](figures/lec9/kademlia-routing-2.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 3](figures/lec9/kademlia-routing-3.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 4](figures/lec9/kademlia-routing-4.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 5](figures/lec9/kademlia-routing-5.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 6](figures/lec9/kademlia-routing-6.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 7](figures/lec9/kademlia-routing-7.svg)
]
]

---

class: middle, center

### A new node `011000` is involved with a RPC message.

.center[
.width-100[
![Kademlia Routing 8](figures/lec9/kademlia-routing-8.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 9](figures/lec9/kademlia-routing-9.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 10](figures/lec9/kademlia-routing-10.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 11](figures/lec9/kademlia-routing-11.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 12](figures/lec9/kademlia-routing-12.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 13](figures/lec9/kademlia-routing-13.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 14](figures/lec9/kademlia-routing-14.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 15](figures/lec9/kademlia-routing-15.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 16](figures/lec9/kademlia-routing-16.svg)
]
]

---

class: middle, center

.center[
.width-100[
![Kademlia Routing 17](figures/lec9/kademlia-routing-17.svg)
]
]

---

# Kademlia Summary

- Efficient, guaranteed look-ups $\mathcal{O}(\text{log} N)$
- XOR-based metric topology (provable consistency and performance).
- Possibly latency minimizing (by always picking the lowest latency note when selecting $\alpha$ nodes).
- Lookup is iterative, but concurrent ($\alpha$).
- Kademlia protocol implicitly enables data persistence and recovery, no special failure mechanisms requires.
- Flexible routing table robust against DoS (route table flushing).

---

class: end-slide, center
count: false

The end.

---

# References

- https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf (Chord)
- https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf (Kademlia)
