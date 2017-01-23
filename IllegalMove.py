class IllegalMove(Exception):
    """A custom exception for indicating a generic illegal move
    Note:
    Args:
    *args (str): A string to return
    **kwargs (obj): Code to return
    Attributes:
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class IllegalKo(IllegalMove):
    """A custom exception for indicating a illegal ko move
    Note:
    Args:
    *args (str): A string to return
    **kwargs (obj): Code to return
    Attributes:
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class IllegalMoveAlreadyMade(IllegalMove):
    """A custom exception for indicating a illegal move to a
        position on the board that is already occupied.
    Note:
    Args:
    *args (str): A string to return
    **kwargs (obj): Code to return
    Attributes:
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
