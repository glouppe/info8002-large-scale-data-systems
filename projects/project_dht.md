class: middle, center, title-slide

# Large-scale Distributed Systems

## Project: Distributed Hash Table

Fall 2017

---

class: center, middle

## Build your own Distributed Hash Table

---

# Group Formation

- Groups of one or two persons.
- Please register your group at ![http://submit.montefiore.ulg.ac.be](http://submit.montefiore.ulg.ac.be) for the DHT project.

**Group Formation Deadline**: 12th of November.

---

# Constraints

To make your life a little bit easier, we will impose some constraints with regards to network programming.

Meaning, instead of having to program a custom network protocol, you will have to build a small REST API to exchange information with other peers. This also makes the verification process easier.

---

# Endpoints

These are the API endpoints you *have* to implement:

- `/fetch/[hash]` (GET)
- `/identifier` (GET)
- `/key/[hash]` (GET)
- `/keys` (GET)
- `/ping` (GET)
- `/state` (GET)
- `/store` (POST)
- `/store/local` (POST)

---

# `/fetch/[hash]`

- `GET`
- Fetches the value for the specified hash, possibly looks over the complete network.
- Can respond in two ways:
  - HTTP 404 (empty response) if specified hash is not found in the DHT.
  - HTTP 200:
  ```json
  {
    "key": "[hash]",
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

# `/key/[hash]`

- `GET`
- Returns HTTP 404 if the *process* does not hold the specified identifier.
- Returns HTTP 200 with the following payload if the *process* hold the key:
```json
{
  "key": "[hash]",
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
        {"key": "[hash]", "value": {whatever}},
        {"key": "[hash]", "value": {whatever}}
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
    "key": "[hash]",
    "value": {whatever}
}
```
- After accepting the message, it should store the specified `key` and `value` in the DHT.

---

# `/store/local`

- Identical behaviour to the `/store` endpoint.
- With the difference that it will force a store on the *process* level.

# Deliverables

- A *report* (pdf) describing your architecture, implementation, and experiments you conducted.
- A *zip* file containing your implementation.

---

# Evaluation Criteria

- Resilliance against failures.
  - Number of nodes that can fail before data is lost.
- Scalability.
  - Routing (number of nodes that have to be contacted before key is found).
- Report Quality
  - Experiments (see above)
  - Architecture description
  - Method

---

class: middle, center

## Deadline: 31 December 2017 at 23:59:59

### Submit to: submit.montefiore.ulg.ac.be

---

class: middle, center

## Have Fun!

---
