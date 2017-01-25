#!/usr/bin/env python

import numpy as np
import sys
import re
import GameState as gs
from operator import itemgetter

# All keys above 100 are not used
sgf_dict = dict([
    ("AN", 101),    # Annotations -> Trash
    ("AP", 102),    # Application -> Trash
    ("BT", 103),    # name of black team -> Trash
    ("C", 104),     # Comment -> Trash
    ("CP", 105),    # copyright
    ("EV", 106),    # Name of event -> Trash
    ("ON", 107),    # Information about opening -> Trash
    ("RO", 108),    # Round(e.g. 5th game) -> Trash
    ("SO", 109),    # Source of sgf -> Trash
    ("US", 110),    # Creator of sgf -> Trash
    ("WT", 111),    # Name of white team
    ("\n", 112),    # Blank new line
    ('', 25),      # No Space
    ("AB", 1),      # Add Black piece before game start
    ("AW", 2),      # Add White piece before game start
    ("B", 3),      # A move by black at position
    ("BR", 4),      # Rank of black player
    ("DT", 5),      # Date and Time of game
    ("FF", 6),      # File format
    ("GM", 7),      # Type of game 1 == go
    ("GN", 8),      # Name of the game record
    ("HA", 9),      # Handicap for black
    ("KM", 10),     # Komi
    ("OT", 10),     # Overtime System
    ("PB", 11),     # Name of Black Player
    ("PC", 12),     # Place game was played
    ("PL", 13),     # Color of player to start
    ("PW", 14),     # Name of white player
    ("RE", 15),     # Result of game
    ("RU", 16),     # Ruleset
    ("SZ", 17),     # Size of the board
    ("TB", 18),     # Black territory at the end of the game
    ("TM", 19),     # Time Limit in seconds
    ("TW", 20),     # White territory at the end of the game
    ("W", 21),     # A move by white at position
    ("WR", 22),     # Rank of white player
    ("(;\n", 23),     # Start of File
    (")\n", 24)       # End of file
])

class TrainingGame():
    """ Class TrainingGame

    Used for converting .sgf files into Tensor inputs

    """
    def __init__(self, filename):
        """ Creates a TrainingGame from file $filename
        """
        pastSize = False
        file = open(filename, "r")
        linenumber = 0

        for line in file.readlines():
            if pastSize:
                line_segments = line.split(";")
            else:
                line_segments = line.split("[")
            case = sgf_dict[line_segments[0]]
            print(case, line_segments)
            if case > 100:
                continue
            elif case == 25:
                case = sgf_dict[line_segments[1].split('[')[0]]
            if case == 1:
                BlackHandicap = line_segments
            elif case == 23:
                print("Start of File")
            elif case == 24:
                print("End of File")
                char = re.search(r'\d+', line).group()
                print(char)
                self.format = int(char)
                print(self.format)
            elif case == 17 and not pastSize:
                self.boardLength = 1
                pastSize = True
                continue
            #elif linenumber == 2:
            else:
                continue
            linenumber += 1

TG = TrainingGame("Games/game0.sgf")
