import sgf
import multiprocessing as mp
import numpy as np
import random
import sys
import array
import os

class SGFSerializer():
    """

        Class for creating serialized training data from sgf files

    """
    def __init__(self, boardSize):
        """
        Init Method
        """
        self.boardSize = boardSize
        self.pos = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def addOneFile(self, filename):
        game = sgf.Collection()
        with open(filename, 'r', encoding='utf-8', errors='ignore') as F:
            game = sgf.parse(F.read())
        return game.children[0]

    def addFile(self, number):        
        filename = "../CSV-re/game"+str(number)+".sgf"
        game = sgf.Collection()
        with open(filename, 'r', encoding='utf-8', errors='ignore') as F:
            game = sgf.parse(F.read())
        return game.children[0]

    def writeCSV(self, game_tree, index):
        filename = "../CSV-temp-"+str(self.boardSize)+'x'+str(self.boardSize)+"/go-data"+str(index)+".csv"
        #print ("Parse file "+str(index)+"\n")
        with open(filename, 'w', encoding='utf-8', errors='ignore') as F:
            game_state_win = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]
            game_state_lose = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]
            try:
                 try:
                     try:
                          first = True
                          for node in game_tree:
                              if node.first:
                                  if self.boardSize == 19:
                                      try: 
                                          size = node.properties["SZ"]
                                          if size == [str(self.boardSize)]:
                                              winner = node.properties["RE"][0].split('+')[0]
                                              if winner == 'W':
                                                  loser = 'B'
                                              else:
                                                  loser = 'W'
                                          else:
                                              os.remove(filename)
                                              break;
                                      except KeyError:
                                          try:
                                              winner = node.properties["RE"][0].split('+')[0]
                                              if winner == 'W':
                                                  loser = 'B'
                                              else:
                                                  loser = 'W'
                                          except KeyError:
                                              sys.stderr.write("Key error for 'RE' in file "+str(index)+"\n")
                                              os.remove(filename)
                                              break;
                                  elif node.properties["SZ"] != [str(self.boardSize)]:
                                      os.remove(filename)
                                      break;
                                  else:
                                      winner = node.properties["RE"][0].split('+')[0]
                                      if winner == 'W':
                                          loser = 'B'
                                      else:
                                          loser = 'W'
                                  first = False
                              else:
                                  try:
                                      try:
                                          move = node.properties[winner][0]
                                          col = ord(move[0]) - 96
                                          row = ord(move[1]) - 96
                                          game_state_win[row][col] = 1
                                          for x in range(self.boardSize):
                                              for y in range(self.boardSize):
                                                  F.write(str(game_state_lose[x][y])+' ')
                                          #for x in range(self.boardSize):
                                          #    for y in range(self.boardSize):
                                          #        F.write(str(game_state_win[x][y])+' ')
                                          F.write('\n')
                                          game_state_lose[row][col] = 1
                                          # Reset the solution action
                                          game_state_win[row][col] = 0
                                      except KeyError:
                                          move = node.properties[loser][0]
                                          col = ord(move[0]) - 96
                                          row = ord(move[1]) - 96
                                          game_state_lose[row][col] = -1
                                          #game_state_win[row][col] = -1
                                  except KeyError:
                                      sys.stderr.write("Key error for B or W in file "+str(index)+"\n")
                                      break;
                     except IndexError:
                         if First:
                             os.remove(filename)
                         return
                 except KeyError:
                    if First:
                        os.remove(filename)
                    return 
            except Exception as err:
                if First:
                    os.remove(filename)
                return
        return

    def convertFile(self, index):
        try:
            game = self.addFile(index)
            self.writeCSV(game, index)
        except Exception:
            print("File "+str(index)+" failed\n")
            sys.stderr.write("Error proxessing"+str(index)+"\n")

    def convertFiles(self, num_files):
        pool = mp.Pool()
        for i, _ in enumerate(pool.imap_unordered(self.convertFile, range(num_files)), 1):
            try:
                sys.stderr.write('\rProcessed {0} of {1}'.format(i,num_files))
            except Exception as err:
                sys.stderr.write('Processing next file')

    def convertFilesNoT(self, num_files):
        for i in range(150000, num_files):
            print ("Convert "+str(i))
            self.convertFile(i)

