# Large-Scale Distributed Systems: Exercise Session 2

## About the previous exercise session

**Note:** https://linux.die.net/man/3/setsockopt http://www.tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO/

## About the current exercise session

**Note**: Delivering and receiving messages are 2 different concepts in the book. I didn't realized either until I was preparing these exercises.

## Exercise 1

Best-Effort Broadcast is a broadcast primitive with a weak form of reliability. In this setting, the burden of ensuring reliable delivery is only on the sender. Therefore, the remaining processes do not have to be concered with enforcing the reliability of received messages among other nodes. Which in turn results in the fact that there are not delivery guarentees when the sender fails.

Delivery of a message is only ensured whenever the sender is *correct*. That it, it didn't crash, or it does not behave in a malicious way (e.g., by excluding a set of particular processes). Given the fact that the sender is *correct*, delivery of the message is ensured by a *perfect link* between the sender and a participating node.

**Note**: the following architecture I'm describing here is not the only solution.

- Nodes are interconnected using TCP with a heartbeat protocol or SO_KEEPALIVE with a reduced time-out window. Broadcast is implemented by establishing a connection with all other n - 1 nodes, and transferring the data.

## Exercise 2

Duplication in Best-Effort Broadcast does **not** occur in Best-Effort Broadcast since the *no duplication* property from the *perfect link* abstraction (which the best-effort broadcast abstraction uses) ensures that a message is only *delivered* once.

## Exercise 3

The problem which reliable broadcasting solves is the delivery ensurence problem whenever the sender crashes. Reliable broadcast ensures this by incorperating an additional *liveness* property which is called *Agreement* which says that if a message *m* is delivered by some *correct* process, then *m* is eventually *delivered* by every correct process. This means that processes agree on the set of messages they deliver, even when the senders of these messages crash during transmission.

However, in order to ensure the *no duplication* property. A mechanism is required to filter duplicate messages which may be retransmitted by other messages.

So Reliable Broadcast is basically:
* Also adds a *message descriptor* and the *source* to the header of the broadcasted message.
1. Original sender broadcasts *m*
2. Some failures happen.
3. A process *p* checks if it already *delivered* *m*
4. If it didn't retransmit to all other nodes.
5. Add *m* to the send of delivered messages.

## Exercise 4

*Lazy reliable broadcast* and *eager reliable broadcast* are instances of the *reliable regular broadcast* abstraction.

Lazy Reliable Broadcast:
- Keep track of a set of correct nodes.
- The failure detector detects that a node *n* is crashed.
- Retransmit all messages from *s* that where delivered.

Eager Reliable Broadcast:
- No failure detector, basically reliable regular broadcast.

## Exercise 5

Use your creativity (look at bitspace of messages in distributed systems).

## Exercise 6

Again, uniform reliable broadcast ensures that if a message is delivered (by a correct or faulty process), then all correct processes deliver. To accomplish this, a mechanism for message filtering and failure detection is required (in order to detect crashed nodes).

## Exercise 7

No, because messages can still be received and thereby delivered in an unordered fashion because there is no *history* mechanism present. To accomplish this one could use a history of messages, or timestamp the messages using vector clocks.

## Exercise 8

Use your creativity.

## Exercise 9

Use your creativity.
