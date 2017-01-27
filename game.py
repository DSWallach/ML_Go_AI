import sgflib

parser = sgflib.SGFParser("Games/game0.sgf")
collect = parser.parse()
print(collect)
sgflib.selfTest1(0)