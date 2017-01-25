#!/usr/bin/env python

import numpy as np
import sys
import re
from operator import itemgetter

# All keys above 100 are not used
sgf_dict = dict([
    ("AB", 1),    # Add Black piece before game start
    ("AW", 2),    # Add White piece before game start
    ("AN", 101),  # Annotations -> Trash
    ("AP", 102),  # Application -> Trash
    ("B", 3),     # A move by black at position
    ("BR", 4),    # Rank of black player
    ("BT", 103),  # name of black team -> Trash
    ("C", 104),   # Comment -> Trash
    ("CP", 105),  # copyright
    ("DT", 5),    # Date and Time of game
    ("EV", 106),  # Name of event -> Trash
    ("FF", 6),    # File format
    ("GM", 7),    # Type of game 1 == go
    ("GN", 8),    # Name of the game record
    ("HA", 9),    # Handicap for black
    ("KM", 10),   # Komi
    ("ON", 107),  # Information about opening -> Trash
    ("OT", 10),   # Overtime System
    ("PB", 11),   # Name of Black Player
    ("PC", 12),   # Place game was played
    ("PL", 13),   # Color of player to start
    ("PW", 14),   # Name of white player
    ("RE", 15),   # Result of game
    ("RO", 16),   # Round(e.g. 5th game)
    ("RU", 17),   # Ruleset
    ("SO", 108),  # Source of sgf -> Trash
    ("SZ", 18),   # Size of the board
    ("TM", 19),   # Time Limit in seconds
    ("US", 109),  # Creator of sgf
    ("W", 20),    # A move by white at position
    ("WR", 21),   # Rank of white player
    ("WT", 110)   # Name of white team
])

class TrainingGame():
    """ Class TrainingGame

    Used for converting .sgf files into Tensor inputs

    """
    def __init__(self, filename):
        """ Creates a TrainingGame from file $filename
        """

        file = open(filename, "r")
        linenumber = 0

        for line in file.readlines():
            if linenumber == 0:
                linenumber += 1
                continue
            elif linenumber == 1:
                char = re.search(r'\d+', line).group()
                print(char)
                self.format = int(char)
                print(self.format)
            #elif linenumber == 1:
            #elif linenumber == 2:
            #else:
            linenumber += 1

TG = TrainingGame("TrainingData/game0.sgf")
