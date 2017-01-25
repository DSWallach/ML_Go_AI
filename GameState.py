#! /usr/bin/env python
from scipy.spatial import KDTree

def letter2Number(letter):
    return (ord(letter) - 96).lower()

def moveParse(moveString):
    parse_string = moveString.split('[')
    parse_string = parse_string[1].split(']')
    parse_string = parse_string[0].split('')
    col = letter2Number(parse_string[0])
    row = letter2Number(parse_string[1])
    return [col, row]

class GameState():
    """ A class for recording each state of a Game 

    """
    def __init__(self, boardSize, winner, move):
        """ Initialization for the first state of a game """
        self.boardSize = boardSize
        self.winner = winner
        boardList = list()
        for i in range(boardSize):
            col = list()
            for j in range(boardSize):
                col.append(0)
            boardList.append(row)
        self.gameBoard = boardList
        return self

    def __init__(self, prevState, move):
        """ Initialization from a previous gameState """
        self.boardSize = boardSize
        self.winner = winner
        for i in range(boardSize):
            for j in range(boardSize):
                continue
        return self
    