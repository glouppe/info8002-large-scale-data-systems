import hashlib
import numpy as np



def hash(object):
    data = bytearray(object)
    hasher = hashlib.sha512()
    hasher.update(data)

    return hasher.hexdigest()
