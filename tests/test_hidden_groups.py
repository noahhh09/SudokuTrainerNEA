from src.analysis.techniques.HiddenGroup import HiddenPair
from src.core.BoardState import BoardState

# Basic Hidden Pair in a row
state1 = BoardState.deserialise(
    "5f3f4fx28f9f1f2f/6f7f2f1f9f5f3f4fx1/1f9f8f3f4f2f5f6f7f/8f5fx44f2f3f/4f2f6f8f5f3f7f9f1f/x42fx18f5f6f/9f6fx15f3f7fx18fx1/2f8f7f4f1f9f6f3f5f/3f4f5f2f8f6f1f7f9f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(ROW 3 POSITIONS{3, 4} DIGITS{6, 7}, [EliminationChangeMove(3, 3, 9, True)])]
print("\n1")
print(HiddenPair.findAvailable(state1))


# Basic Hidden Pair in a column
state2 = BoardState.deserialise(
    "x13f4f6f7f8fx11f2f/6fx12f1fx15f3fx18f/1f9fx13f4fx15f6f7f/8fx19f7f6fx14f2f3f/4f2f6fx15f3f7f9f1f/x23f9fx14f8fx16f/9f6f1f5f3f7f2f8f4f/2fx17f4f1f9f6f3f5f/3f4f5f2f8f6f1f7f9f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(COLUMN 1 POSITIONS{3, 5} DIGITS{1, 5}, [EliminationChangeMove(5, 1, 7, True)])]
print("\n2")
print(HiddenPair.findAvailable(state2))


# Basic Hidden Pair in a block
state3 = BoardState.deserialise(
    "5f3f4f6f7f8fx11fx1/6f7f2f1f9f5fx14f8f/x19fx13f4fx15f6f7f/8f5f9f7fx24f2fx1/4f2f6fx15fx17f9f1f/7f1f3fx12f4f8f5fx1/9f6f1f5f3f7f2f8f4f/2f8f7f4fx19f6f3f5f/3f4f5f2f8fx11f7f9f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(BLOCK 4 POSITIONS{1, 2} DIGITS{1, 6}, [EliminationChangeMove(3, 5, 3, True)])]
print("\n3")
print(HiddenPair.findAvailable(state3))


# Hidden Pair where both causal cells contain different extra candidates
state4 = BoardState.deserialise(
    "5f3f4f6f7f8f9f1f2f/6fx12fx19f5fx14f8f/1f9f8f3f4f2f5f6f7f/8fx19fx16f1fx12f3f/4f2fx18f5f3f7f9f1f/7fx29f2f4f8fx2/9f6f1f5f3f7f2f8fx1/2f8fx14f1fx16f3f5f/x14fx12f8fx11fx19f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(COLUMN 2 POSITIONS{5, 8} DIGITS{3, 5},
#     [EliminationChangeMove(5, 2, 6, True),
#      EliminationChangeMove(8, 2, 7, True)])]
print("\n4")
print(HiddenPair.findAvailable(state4))


# Hidden Pair where both causal cells share the same extra candidate
state5 = BoardState.deserialise(
    "x13f4f6fx18f9fx12f/x17f2fx25f3f4fx1/x19f8f3f4f2fx27f/8f5f9f7fx11f4f2f3f/4f2f6f8f5f3f7f9f1f/7f1f3fx12f4f8fx16f/x16f1f5f3fx12f8f4f/2f8f7f4f1f9f6f3f5f/3f4f5f2f8f6f1f7f9f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(ROW 2 POSITIONS{0, 7} DIGITS{1, 6},
#     [EliminationChangeMove(2, 0, 5, True),
#      EliminationChangeMove(2, 7, 5, True)])]
print("\n5")
print(HiddenPair.findAvailable(state5))


# Hidden Pair occurring late in a unit
# Useful for testing that failed earlier combinations do not prevent later ones being checked
state6 = BoardState.deserialise(
    "5f3f4f6f7f8f9f1fx1/6f7f2f1fx15fx14f8f/1f9f8f3f4fx15fx17f/8f5f9f7f6f1f4f2f3f/4f2f6f8f5f3f7f9f1f/7f1f3f9f2f4f8f5f6f/9f6f1f5fx17fx24f/2f8f7f4fx45f/3f4f5f2f8fx27f9f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(COLUMN 6 POSITIONS{7, 8} DIGITS{1, 6}, [EliminationChangeMove(7, 6, 3, True)])]
print("\n6")
print(HiddenPair.findAvailable(state6))


# Hidden Pair at opposite ends of a unit
state7 = BoardState.deserialise(
    "x36f7f8f9f1f2f/6f7f2f1f9f5fx14f8f/1fx18f3f4f2f5f6f7f/8f5f9f7f6f1fx12f3f/x12f6f8f5f3f7f9f1f/x11f3f9f2fx18f5f6f/9f6f1f5f3f7f2fx14f/x18f7f4f1fx16f3f5f/x32f8f6f1f7f9f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(COLUMN 0 POSITIONS{0, 8} DIGITS{3, 5},
#     [EliminationChangeMove(0, 0, 4, True),
#      EliminationChangeMove(8, 0, 4, True)])]
print("\n7")
print(HiddenPair.findAvailable(state7))


# Hidden Pair requiring more than one candidate to be eliminated from a causal cell
state8 = BoardState.deserialise(
    "5f3f4f6fx18f9fx2/6f7f2f1f9fx13f4fx1/1f9fx13f4f2f5f6f7f/8f5f9f7f6f1f4f2f3f/4f2f6f8fx13f7f9f1f/7f1fx19f2f4f8f5f6f/9fx25f3f7f2f8f4f/2fx24fx26fx15f/x32f8fx11fx19f"
)
# Expected:
# 1 Hidden Pair
# [HiddenPair(ROW 7 POSITIONS{2, 7} DIGITS{3, 7},
#     [EliminationChangeMove(7, 2, 1, True),
#      EliminationChangeMove(7, 2, 8, True)])]
print("\n8")
print(HiddenPair.findAvailable(state8))


# Two separate Hidden Pairs
# The same cell participates in both
state9 = BoardState.deserialise(
    "5f3f4fx17f8f9f1f2f/x17f2fx19f5fx14fx1/x19fx24f2f5f6f7f/8f5fx26f1f4fx13f/x12f6f8f5f3f7f9fx1/7f1fx19f2f4f8f5f6f/9f6f1f5f3f7f2f8fx1/2f8fx39f6f3f5f/3fx15fx18f6f1f7f9f"
)
# Expected:
# 2 Hidden Pairs
# [
#     HiddenPair(ROW 1 POSITIONS{0, 3} DIGITS{1, 6},
#         [EliminationChangeMove(1, 3, 3, True)]),
#
#     HiddenPair(BLOCK 1 POSITIONS{3, 6} DIGITS{1, 3},
#         [EliminationChangeMove(1, 3, 6, True)])
# ]
print("\n9")
print(HiddenPair.findAvailable(state9))


# Same logical Hidden Pair is valid in both a column and a block
state10 = BoardState.deserialise(
    "5f3f4f6f7f8fx11f2f/6f7fx29f5f3f4f8f/x19fx24fx15fx17f/8f5fx17f6fx14f2f3f/x26f8f5f3fx19f1f/x23f9f2fx18f5f6f/9f6f1f5f3f7f2f8f4f/2f8f7f4f1f9f6f3f5f/3f4f5f2f8f6fx29f"
)
# Expected:
# 2 Hidden Pairs
# [
#     HiddenPair(COLUMN 0 POSITIONS{4, 5} DIGITS{4, 7},
#         [EliminationChangeMove(5, 0, 1, True)]),
#
#     HiddenPair(BLOCK 3 POSITIONS{3, 6} DIGITS{4, 7},
#         [EliminationChangeMove(5, 0, 1, True)])
# ]
print("\n10")
print(HiddenPair.findAvailable(state10))


# Three Hidden Pair results on one board
state11 = BoardState.deserialise(
    "5fx26f7fx19f1f2f/x17f2fx19f5fx14f8f/x19fx24f2f5f6f7f/8f5f9f7f6fx14f2f3f/4f2f6fx15fx4/x11f3f9f2f4fx15fx1/x16f1f5f3fx12fx2/x18f7f4fx19fx13f5f/3f4f5f2f8f6f1f7f9f"
)
# Expected:
# 3 Hidden Pairs
# [
#     HiddenPair(COLUMN 5 POSITIONS{0, 4} DIGITS{3, 8},
#         [EliminationChangeMove(4, 5, 1, True)]),
#
#     HiddenPair(COLUMN 6 POSITIONS{4, 5} DIGITS{7, 8},
#         [EliminationChangeMove(5, 6, 6, True)]),
#
#     HiddenPair(BLOCK 4 POSITIONS{3, 5} DIGITS{3, 8},
#         [EliminationChangeMove(4, 3, 1, True),
#          EliminationChangeMove(4, 5, 1, True)])
# ]
print("\n11")
print(HiddenPair.findAvailable(state11))


# Four overlapping Hidden Pair results
state12 = BoardState.deserialise(
    "5f3f4fx28fx11f2f/x17f2f1f9f5f3f4f8f/1fx18f3f4f2f5f6f7f/x15f9fx34fx13f/4f2f6fx15f3f7f9fx1/7f1f3fx38f5f6f/9f6f1f5f3f7f2f8f4f/2f8f7f4f1f9fx13fx1/x14f5f2f8f6f1f7f9f"
)
# Expected:
# 4 Hidden Pairs
# [
#     HiddenPair(ROW 3 POSITIONS{3, 4} DIGITS{6, 7},
#         [EliminationChangeMove(3, 3, 8, True),
#          EliminationChangeMove(3, 4, 2, True)]),
#
#     HiddenPair(COLUMN 3 POSITIONS{0, 3} DIGITS{6, 7},
#         [EliminationChangeMove(3, 3, 8, True)]),
#
#     HiddenPair(COLUMN 4 POSITIONS{0, 3} DIGITS{6, 7},
#         [EliminationChangeMove(3, 4, 2, True)]),
#
#     HiddenPair(BLOCK 4 POSITIONS{0, 1} DIGITS{6, 7},
#         [EliminationChangeMove(3, 3, 8, True),
#          EliminationChangeMove(3, 4, 2, True)])
# ]
print("\n12")
print(HiddenPair.findAvailable(state12))


# Negative control - no Hidden Pairs
state13 = BoardState.deserialise(
    "5f3f4f6f7f8f9f1f2f/6f7fx11f9f5f3f4f8f/1f9f8f3f4f2f5f6f7f/8f5f9f7f6f1f4f2fx1/x12fx18f5f3f7f9fx1/7f1f3f9f2f4f8f5f6f/9f6f1f5f3f7f2f8fx1/x18fx14f1f9f6fx15f/3f4fx12f8f6f1f7f9f"
)
# Expected:
# No Hidden Pairs
# []
print("\n13")
print(HiddenPair.findAvailable(state13))


# Structurally a Hidden Pair, but there is nothing to eliminate
# The two cells already contain exactly {2, 5}
state14 = BoardState.deserialise(
    "5fx14f6f7f8f9f1f2f/6f7f2f1f9f5f3f4f8f/1f9f8f3f4f2f5f6f7f/8f5f9f7f6f1f4fx13f/4f2f6f8fx13f7f9f1f/7f1f3f9fx28fx16f/9f6f1f5f3f7f2f8f4f/2f8f7f4fx19f6f3fx1/3f4f5fx18f6f1fx19f"
)
# Structurally:
# HiddenPair(ROW 5 POSITIONS{4, 7} DIGITS{2, 5}, [])
#
# Expected from findAvailable(), because no eliminations are possible:
# []
print("\n14")
print(HiddenPair.findAvailable(state14))


# Naked Pair exists, but it is NOT a Hidden Pair
# The pair's digits are not restricted to only those two cells
state15 = BoardState.deserialise(
    "5f3f4fx17f8f9f1f2f/6f7f2f1f9f5fx14f8f/1f9f8f3f4f2f5fx17f/8f5f9f7f6f1f4f2fx1/4f2f6f8f5f3fx19f1f/7f1f3f9f2f4f8f5f6f/9f6f1f5fx17f2f8f4f/2f8f7f4f1fx4/3f4f5f2f8f6f1f7f9f"
)
# Expected:
# No Hidden Pairs
# []
print("\n15")
print(HiddenPair.findAvailable(state15))


# Completely blank board
state16 = BoardState.deserialise(
    "x9/x9/x9/x9/x9/x9/x9/x9/x9"
)
# Expected:
# No Hidden Pairs
# []
print("\n16")
print(HiddenPair.findAvailable(state16))


# Completely solved board
state17 = BoardState.deserialise(
    "5f3f4f6f7f8f9f1f2f/6f7f2f1f9f5f3f4f8f/1f9f8f3f4f2f5f6f7f/8f5f9f7f6f1f4f2f3f/4f2f6f8f5f3f7f9f1f/7f1f3f9f2f4f8f5f6f/9f6f1f5f3f7f2f8f4f/2f8f7f4f1f9f6f3f5f/3f4f5f2f8f6f1f7f9f"
)
# Expected:
# No Hidden Pairs
# []
print("\n17")
print(HiddenPair.findAvailable(state17))