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
    def __init__(self, path, dest, boardSize, value):
        """
        Init Method
        """
        self.boardSize = boardSize
        self.path = path
        self.dest = dest
        self.pos = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.value = value

    def addFile(self, number):        
        filename = self.path+"/game"+str(number)+".sgf"
        game = sgf.Collection()
        with open(filename, 'r', encoding='utf-8', errors='ignore') as F:
            game = sgf.parse(F.read())
        return game.children[0]

    def writeCSV(self, game_tree, index):
        filename = self.dest+"/go-data"+str(index)+".csv"
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
                                  # Filter by player rank, ignore games between kyu players
                                  if "k" in node.properties["BR"] and "k" in node.properties["WR"]:
                                      std.err.write("Game between kyus") 
                                      os.remove(filename)
                                      break
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
                                        # Starting characters for a lisp vector
                                          F.write("#(")
                                          for x in range(self.boardSize):
                                              for y in range(self.boardSize):
                                                  F.write(str(game_state_lose[x][y])+' ')
# Close the vecotr
                                          F.write(")")
                                          F.write("#(")
                                          for x in range(self.boardSize):
                                              for y in range(self.boardSize):
                                                  if x == row and y == col:
                                                      F.write(str(1)+' ')
                                                  else:
                                                      F.write(str(0)+' ')
                                                  #F.write(str(game_state_win[x][y])+' ')
                                          F.write(")")
                                          F.write('\n')
                                          game_state_lose[row][col] = 1
                                          # Reset the solution action
                                          #game_state_win[row][col] = 0
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
                         if node.first:
                             os.remove(filename)
                         return
                 except KeyError:
                     if node.first:
                         os.remove(filename)
                     return 
            except Exception as err:
                if node.first:
                    os.remove(filename)
                return
        return

    def writeCSVvalue(self, game_tree, index):
        filename = self.dest+"/go-data"+str(index)+".csv"
        #print ("Parse file "+str(index)+"\n")
        with open(filename, 'w', encoding='utf-8', errors='ignore') as F:
            game_state = [[0 for x in range(self.boardSize)] for y in range(self.boardSize)]
            try:
                 try:
                     try:
                          first = True
                          for node in game_tree:
                              if node.first:
                                  # Filter by player rank, ignore games between kyu players
                                  if "k" in node.properties["BR"] and "k" in node.properties["WR"]:
                                      std.err.write("Game between kyus") 
                                      os.remove(filename)
                                      break
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
                              else:
                                  try:
                                      try:
                                          move = node.properties[winner][0]
                                          col = ord(move[0]) - 96
                                          row = ord(move[1]) - 96
                                          game_state[row][col] = 1
                                        # Starting characters for a lisp vector
                                          F.write("#(")
                                          for x in range(self.boardSize):
                                              for y in range(self.boardSize):
                                                  F.write(str(game_state[x][y])+' ')
                                          F.write(")")
                                          F.write("#(")
                                          if winner == 'B':
                                              F.write("1")
                                          else:
                                              F.write("-1")
                                          F.write(")")
                                          F.write('\n')
                                      except KeyError:
                                          move = node.properties[loser][0]
                                          col = ord(move[0]) - 96
                                          row = ord(move[1]) - 96
                                          game_state[row][col] = -1
                                          F.write("#(")
                                          for x in range(self.boardSize):
                                              for y in range(self.boardSize):
                                                  F.write(str(game_state[x][y])+' ')
                                          F.write(")")
                                          F.write("#(")
                                          if winner == 'B':
                                              F.write("1")
                                          else:
                                              F.write("-1")
                                          F.write(")")
                                          F.write('\n')
                                  except KeyError:
                                      sys.stderr.write("Key error for B or W in file "+str(index)+"\n")
                                      break;
                     except IndexError:
                         sys.stderr.write("Index error in file "+str(index)+"\n")
                         if node.first:
                             os.remove(filename)
                         return
                 except KeyError:
                     sys.stderr.write("Key error in file "+str(index)+"\n")
                     if node.first:
                         os.remove(filename)
                     return 
            except Exception as err:
                sys.stderr.write("Error in file "+str(index)+"\n")
                if node.first:
                    os.remove(filename)
                return
        return

    def convertFile(self, index):
        try:
            game = self.addFile(index)
            if self.value:
                self.writeCSVvalue(game, index)
            else:
                self.writeCSV(game, index)
        except Exception:
            return index

    def convertFiles(self, num_files):
        pool = mp.Pool()
        for i, _ in enumerate(pool.imap_unordered(self.convertFile, range(num_files)), 1):
            try:
                sys.stderr.write('\rProcessed {0} of {1}'.format(i,num_files))
            except Exception as err:
                sys.stderr.write('Processing next file')

    def convertFilesNoT(self, num_files):
        errored = list()
        for i, _ in enumerate(range(0, num_files), 1):
            sys.stderr.write('\rProcessed {0} of {1}'.format(i,num_files))
            errored.append(self.convertFile(i))

