class: middle, center, title-slide

# Large-scale Distributed Systems

## Project: Distributed Hash Table

Fall 2017

---

class: center, middle

## Build your own Distributed Hash Table

---

# Constraints

To make your life a little bit easier, we will impose some constraints with regards to network programming.

Meaning, instead of having to program a custom network protocol, you will have to build a small REST API to exchange information with other peers. This also makes the verification process easier.

---

# Endpoints

These are the API endpoints you *have* to implement:

- `/fetch/[hash]` (GET)
- `/identifier` (GET)
- `/keys` (GET)
- `/ping` (GET)
- `/state` (GET)
- `/store` (POST)

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

---

# Deliverables

- A *report* (pdf) describing your architecture, implementation, and experiments you conducted.
- A *zip* file containing your implementation.

---

class: middle, center

## Deadline: 31 December 2017 at 23:59:59

### Submit to: submit.montefiore.ulg.ac.be

---

class: middle, center

## Have Fun!

---
