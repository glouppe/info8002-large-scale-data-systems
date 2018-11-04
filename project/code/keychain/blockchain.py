import hashlib
import multilib
import numpy as np

from keychain.util import hash



class Block:

    def __init__(self, index, proof, transactions=[], previous_hash=None):
        self._index = index
        self._data = {}
        for transaction in transactions:
            self._data[transaction.key] = transaction.value
        self._transactions = transactions
        self._previoius_hash = previous_hash
        self._proof = proof

    def index(self):
        return self._index

    def proof(self):
        return self._proof

    def transactions(self):
        return self._transactions

    def transaction_hashes(self):
        return [t.hash() for t in self._transactions]

    def timestamp(self):
        return self._timestamp

    def hash(self):
        return hash(self)

    def keys():
        return self._data.keys()

    def value(self, key):
        return self._data[key]

    def __getitem__(self, key):
        return self.value(key)

    def is_valid(self):
        raise NotImplementedError


class Transaction:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def hash(self):
        return hash(self)


class Peer:

    def __init__(self, address):
        self._address = address


class Blockchain:


    def __init__(self, bootstrap, difficulty):
        # Initialize the properties.
        self._blocks = []
        self._difficulty = difficulty
        self._peers = []
        self._transactions = []
        # Initialize the chain with the Genesis block.
        self._add_genesis_block()
        # Bootstrap the chain with the specified bootstrap address.
        self._bootstrap(bootstrap)

    def _add_genesis_block(self):
        genesis_transactions = []
        genesis_transactions.append(
            Transaction("baryogenesis", "https://en.wikipedia.org/wiki/Baryogenesis"),
            Transaction("leptogenesis", "https://en.wikipedia.org/wiki/Leptogenesis_(physics)")
            Transaction("lemaitre", "https://en.wikipedia.org/wiki/Georges_Lema%C3%AEtre"),
            Transaction("hubble", "https://en.wikipedia.org/wiki/Edwin_Hubble")
        )
        genesis_proof = hash("whatever")
        previous_hash = hash("emptiness")
        genesis_block = Block(genesis_proof, genesis_transactions, previous_hash)
        self._blocks.append(genesis_block)

    def _bootstrap(self, address):
        peer = Peer(address)
        raise NotImplementedError

    def difficulty(self):
        return self._difficulty

    def add_transaction(self, transaction):
        raise NotImplementedError

    def add_peer(self, peer):
        self._peers.append(peer)

    def remove_peer(self, peer):
        self._peers.remove(peer)

    def is_valid(self):
        # Check if every block of the chain is valid, and if the subsequent hashes match.
        raise NotImplementedError

    def add_transaction(self, transaction):
        raise NotImplementedError
        ## TODO Remove.
        self._transactions.append(transaction)

    def size(self):
        return len(self._blocks)

    def blocks(self):
        return list(self._blocks)

    def __getitem__(self, index):
        return self._blocks[index]
