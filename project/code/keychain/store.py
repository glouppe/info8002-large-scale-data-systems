import numpy as np

from keychain import Blockchain
from keychain import Transaction


class Callback:

    def __init__(self, transaction, chain):
        self._transaction = transaction
        self._chain = chain

    def wait(self):
        # Wait until the transaction appears in the blockchain.
        raise NotImplementedError

    def completed(self):
        # Polls to blockchain to check if the data is available.
        raise NotImplementedError


class Storage:

    def __init__(bootstrap, miner=False, difficulty=5)
        # Allocate the blockchain storage.
        self._blockchain = Blockchain(
            bootstrap=bootstrap,
            difficulty=difficulty
        )

    def put(self, key, value, block=True):
        transaction = Transaction(key, value)
        self._blockchain.add_transaction(self, transaction)
        callback = Callback(transaction, self._blockchain)
        if block:
            callback.wait()

        return callback

    def retrieve(self, key):
        raise NotImplementedError

    def retrieve_all(self, key):
        raise NotImplementedError
