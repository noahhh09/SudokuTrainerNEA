from src.core.BoardState import BoardState
from src.analysis.Contradictions import detectContradictions


state1 = BoardState.deserialise("1tx8/x12tx7/x23tx6/x34tx5/x45tx4/x56tx3/x67tx2/x78tx1/x89t") # Expects no contradiction
state2 = BoardState.deserialise("5tx35tx4/x9/x9/x9/x9/x9/x9/x9/x9") # Expects contradiction (ROW 0) at (0,0) and (0,4)
state3 = BoardState.deserialise("5tx8/x9/x9/x9/5tx8/x9/x9/x9/x9") # Expects contradiction (COL 0) at (0,0) and (4,0)
state4 = BoardState.deserialise("5tx8/x15tx7/x9/x9/x9/x9/x9/x9/x9") # Expects contradiction (BLK 0) at (0,0) and (1,1)
state5 = BoardState.deserialise("5tx35tx4/x9/x9/x9/5tx8/x9/x9/x9/x9") # Expects contradictions [(ROW 0) at (0,0) and (0,4)] WITH [(COL 0) at (0,0) and (4,0)]
state6 = BoardState.deserialise("5tx15tx6/x9/x9/x9/x9/x9/x9/x9/x9") # Expects contradictions [(ROW 0) at (0,0) and (0,2)] WITH [(BLK 0) at (0,0) and (0,2)]
state7 = BoardState.deserialise("5tx8/x9/5tx8/x9/x9/x9/x9/x9/x9") # Expects contradictions [(COL 0) at (0,0) and (2,0)] WITH [(BLK 0) at (0,0) and (2,0)]
state8 = BoardState.deserialise("5tx15tx6/x9/5tx8/x9/x9/x9/x9/x9/x9") # Expects contradictions [ROW 0 at (0,0) and (0,2)] WITH [(COL 0) at (0,0) and (0,2)] WITH [(BLK 0) at (0,0) and (0,2) and (2,0)]

state9 = BoardState.deserialise("5tx15tx55t/x15tx7/5t5tx7/x9/x9/x9/x9/x9/x9") # Expects a lot of contradictions.
print(state9)

print(detectContradictions(state1))
print(detectContradictions(state2))
print(detectContradictions(state3))
print(detectContradictions(state4))
print(detectContradictions(state5))
print(detectContradictions(state6))
print(detectContradictions(state7))
print(detectContradictions(state8))
print(detectContradictions(state9))
