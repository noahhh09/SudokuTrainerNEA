from src.analysis.techniques.HiddenSingle import HiddenSingle
from src.core.BoardState import BoardState


state1 = BoardState.deserialise("x36fx29fx2/6f7f2f1fx23f4f8f/x44f2fx16f7f/x29fx21fx12fx1/x12fx33fx19f1f/7f1f3f9f2f4f8fx16f/x62fx2/2fx24fx26fx15f/x25f2fx37f9f")
state1Found = HiddenSingle.findAvailable(state1)

print(state1)
print(state1Found)
