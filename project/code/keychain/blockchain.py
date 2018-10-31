import hashlib
import multilib
import numpy as np

from keychain.util import hash



class Block:

    def __init__(self, proof, transactions=[], previous_hash=None):
        self._data = {}
        for transaction in transactions:
            self._data[transaction.key] = transaction.value
        self._previoius_hash = previous_hash
        self._proof = proof

    def proof(self):
        return self._proof

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


class Blockchain:


    def __init__(self):
        # Initialize the properties.
        self._transactions = []
        self._blocks = []
        self._peers = []
        # Initialize the chain with the Genesis block.
        self._add_genesis_block()

    def _add_genesis_block(self):
        genesis_transactions = []
        genesis_transactions.append(
            Transaction("baryogenesis", "https://en.wikipedia.org/wiki/Baryogenesis"),
            Transaction("leptogenesis", "https://en.wikipedia.org/wiki/Leptogenesis_(physics)")
            Transaction("lemaitre", "https://en.wikipedia.org/wiki/Georges_Lema%C3%AEtre"),
            Transaction("hubble", "https://en.wikipedia.org/wiki/Edwin_Hubble")
        )
        genesis_proof = hash("no proof required")
        previous_hash = hash("emptiness")
        genesis_block = Block(genesis_proof, genesis_transactions, previous_hash)
        self._blocks.append(genesis_block)

    def add_peer(self, peer):
        self._peers.append(peer)

    def is_valid(self):
        raise NotImplementedError

    def add_transaction(self, transaction):
        raise NotImplementedError
        ## TODO Remove.
        self._transactions.append(transaction)

    def __getitem__(self, index):
        return self._blocks[index]
