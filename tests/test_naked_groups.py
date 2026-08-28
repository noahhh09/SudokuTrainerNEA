from src.analysis.Technique import Technique
from src.analysis.techniques.NakedSingle import NakedSingle
from src.analysis.techniques.NakedGroup import NakedPair, NakedTriple
from src.core.BoardState import BoardState

ALL: list[type[Technique]] = [NakedSingle, NakedPair, NakedTriple]

state1 = BoardState.deserialise(
    "5fx8/6fx12f1fx5/x52fx3/8fx27f6fx33f/x26fx15fx29fx1/x11fx19fx14fx3/x21f5fx17fx3/x66fx2/x89f"
)
for t in ALL:
    print(t.findAvailable(state1))
    # Expected result: one naked single at (3,5) for value 1 ONLY


state2 = BoardState.deserialise(
    "x24fx39f1fx1/x88f/x28fx14f2fx27f/8fx19fx34fx2/x12fx47fx2/x23fx6/x78fx1/x27f4fx19fx13fx1/x32f8f6fx17f9f"
)
for t in ALL:
    print(t.findAvailable(state2))
    # Expected result: one naked pair, ROW 8, group positions {2,6} with candidate union {1,5} ONLY


state3 = BoardState.deserialise(
    "x36fx29fx2/6fx64fx1/1fx23fx36fx1/x15f9fx53f/x45f3fx3/x23fx24fx3/9fx33f7fx24f/x59fx13fx1/x25f2f8fx39f"
)
for t in ALL:
    print(t.findAvailable(state3))
    # Expected result: one naked triple, ROW 8, group positions {5,6,7} with candidate union {1,6,7} ONLY


state4 = BoardState.deserialise(
    "x24fx17f8fx3/x49fx13f4f8f/x28f3fx5/8fx19fx6/x26fx23fx3/x11f3fx12f4f8f5f6f/9fx47f2fx14f/x85f/x9"
)
for t in ALL:
    print(t.findAvailable(state4))
    # Expected result: one naked single at (5,0) for value 7 ONLY. Catches out Naked Pair.


state5 = BoardState.deserialise(
    "x69fx2/6f7fx29fx24fx1/1fx66f7f/x15fx26fx4/x45fx17f9fx1/7fx44fx3/x57f2fx2/2fx24f1fx16fx2/3fx38fx4"
)
for t in ALL:
    print(t.findAvailable(state5))
    # Expected result: one naked single at (6,4) for value 3 ONLY. Catches out Naked Pair and Triple.


state6 = BoardState.deserialise(
    "x69fx2/x17f2fx25fx28f/1fx8/x37f6fx14fx2/4fx43fx21f/x9/x21f5fx17fx18fx1/2fx17fx36fx15f/3fx38fx11f7fx1"
)
for t in ALL:
    print(t.findAvailable(state6))
    # Expected result: NakedPair(COL 0, POSITIONS {1,6}, UNION {6,9}) AND a NakedSingle at (1,6) value 3. Catches out a Naked Pair.

state7 = BoardState.deserialise(
    "x13f4fx28fx3/x55fx14fx1/1f9fx13fx12fx3/x37fx5/x79fx1/x75fx1/9fx68f4f/x34fx19fx13fx1/3fx22fx21fx2"
)
for t in ALL:
    print(t.findAvailable(state7))
    # Expected result: NakedPair(ROW 8, POSITIONS {5,7}, UNION {6,7}) AND NakedPair(COL 7, POSITIONS {2,8}, UNION {6,7}) 

state8 = BoardState.deserialise(
    "5f3f4fx17fx19fx12f/x88f/x9/x15fx44f2fx1/x38fx5/x9/x9/x9/x32fx5"
)
for t in ALL:
    print(t.findAvailable(state8))
    # Expected result: NakedPair(ROW 0, POSITIONS {3,7}, UNION {1,6}) ONLY. Catches out a Naked Triple.

state9 = BoardState.deserialise(
    "x13f4fx52f/6fx12f1f9fx13fx2/1fx34fx26fx1/x37f6f1f4fx2/4fx16fx6/7f1fx22fx4/x16fx23fx34f/x18f7fx11fx4/x14fx57f9f"
)
for t in ALL:
    print(t.findAvailable(state9))
    # Expected result: NakedPair(COL 4, POSITIONS {4,8}, UNION {5,8}) AND NakedTriple(ROW 1, POSITIONS {1,5,8}, UNION {5,7,8}). Catches out a Naked Triple.

state10 = BoardState.deserialise(
    "5f3f4fx41fx1/x49f5f3fx2/1fx23f4fx26f7f/x72f3f/x45f3f7fx11f/x75fx1/x9/x9/x77f9f"
)
for t in ALL:
    print(t.findAvailable(state10))
    # Expected result: NakedTriple(ROW 2, POSITIONS {1,2,5}, UNION {2,8,9}) AND NakedTriple(COL 7, POSITIONS {1,6,7}, UNION {3,4,8}) AND NakedTriple(BLK 2, POSITIONS {idk}, UNION {2,4,8})