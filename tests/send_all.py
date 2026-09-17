from src.analysis import ALL_TECHNIQUE_TYPES
from src.core.BoardState import BoardState


board = BoardState.deserialise(input())
# x26fx28fx3/4fx36fx11f2f8t/8fx32fx16f3fx1/x23f7fx29t4fx1/x51fx18t2f/x54fx15fx1/x59f4fx2/7f4fx51fx1/2fx23fx28fx2
for t in ALL_TECHNIQUE_TYPES:
    print(t, t.findAvailable(board))
