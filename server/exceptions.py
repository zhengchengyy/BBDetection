class DBConnectError(Exception):
    """ Base class for arithmetic errors. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class CollectionError(Exception):
    """ Base class for arithmetic errors. """
    def __init__(self, message):
        self.message = message