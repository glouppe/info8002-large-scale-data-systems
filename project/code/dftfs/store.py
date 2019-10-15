

class Storage:
    def __init__(self, bootstrap):
        """Allocate the backend storage of the high level API."""
        raise NotImplementedError

    def put(self, path, bytes):
        raise NotImplementedError

    def copy(self, source, destination):
        raise NotImplementedError

    def get(self, path):
        raise NotImplementedError

    def exists(self, path):
        raise NotImplementedError
