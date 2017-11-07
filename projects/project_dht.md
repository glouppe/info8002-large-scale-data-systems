class: middle, center, title-slide

# Large-scale Distributed Systems

Project 1: Distributed Hash Table

---

class: center, middle

## Build your own distributed hash table

---

# Group formation

- Groups of one or two persons.
- Register your group at [submit.montefiore.ulg.ac.be](http://submit.montefiore.ulg.ac.be).
- **Group formation deadline**: 12th of November.

---

# Constraints

- To make your life a little bit easier, we will impose some constraints with regards to network programming.
- Instead of having to program a custom network protocol, you will have to build a small REST API to exchange information with other peers.
- This also makes the verification process easier.

---

# Endpoints

These are the API endpoints you must implement:

- `/fetch/[key-identifier]` (GET)
- `/identifier` (GET)
- `/key/[key-identifier]` (GET)
- `/keys` (GET)
- `/ping` (GET)
- `/state` (GET)
- `/store` (POST)
- `/store/local` (POST)

---

# `/fetch/[key-identifier]`

- `GET`
- Fetches the value for the specified key-identifier, querying the DHT if needed.
- Can respond in two ways:
  - HTTP 404 (empty response) if specified hash is not found in the DHT.
  - HTTP 200:
  ```json
  {
    "key": "[key-identifier]",
    "value": {whatever}
  }
  ```

---

# `/identifier`

- `GET`
- Returns the (overlay network) identifier of the current process hosting the webserver.

```json
{"identifier": "0123456789abcdef"}
```

---

# `/key/[key-identifier]`

- `GET`
- Returns HTTP 404 if the *process* does not hold the specified identifier.
- Returns HTTP 200 with the following payload if the *process* hold the key:
```json
{
  "key": "[key-identifier]",
  "value": {whatever}
}
```

---

# `/keys`

- `GET`
- Returns the keys which are associated with the process running the webserver.

```json
{
    "keys": [
        {"key": "[key-identifier]", "value": {whatever}},
        {"key": "[key-identifier]", "value": {whatever}}
    ]
}
```

---

# `/ping`

- `GET`
- Needs to respond with HTTP code 200.
- Used to check if the node is still alive.

---

# `/state`

- `GET`
- Returns the complete state of the current process (includes identifier, keys, and others).

---

# `/store`

- `POST`
- Should accept a `json` of the following format:
```json
{
    "key": "[key-identifier]",
    "value": {whatever}
}
```
- After accepting the message, it should store the specified `key` and `value` in the DHT.

---

# `/store/local`

- Identical behaviour to the `/store` endpoint. Can be viewed as a primitive function.
- With the difference that it will force a store on the *process* level.

---

# Deliverables

- A *report* (pdf, max 5 pages) describing your architecture, implementation, and experiments you conducted.
- A *zip* file containing your implementation.
- Bash script which prints the PID (Process Identifier) and port number of the service for a given number of nodes.

---

# Evaluation criteria

- Resilience against failures.
    - Number of nodes that can fail before data is lost.
- Scalability.
    - Routing (number of nodes that have to be contacted before key is found).
- Report Quality
    - Experiments proving fault-tolerance and scalability.
    - Architecture description.
    - Method:
        - You are free to implement any DHT algorithm.
        - We will evaluate its performance (in terms of resilience and scalability).

---

class: middle, center

## Deadline: 22 December 2017 at 23:59:59

### Submit to [submit.montefiore.ulg.ac.be](http://submit.montefiore.ulg.ac.be).

---

class: middle, center

## Have Fun!
