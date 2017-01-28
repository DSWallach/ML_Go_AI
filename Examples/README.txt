These example are taken from a tutorial found here 
https://indico.io/blog/tensorflow-data-inputs-part1-placeholders-protobufs-queues/

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
    ("AB", 1),      # Add Black piece before game start
    ("AW", 2),      # Add White piece before game start
    (";B", 3),      # A move by black at position
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
    (";W", 21),     # A move by white at position
    ("WR", 22),     # Rank of white player
    ("(;\n", 23),     # Start of File
    (")\n", 24)       # End of file