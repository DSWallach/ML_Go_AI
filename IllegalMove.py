# A custom exception for indicating a illegal move
class IllegalMove(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
class IllegalKo(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,kwargs)
