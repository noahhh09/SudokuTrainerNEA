from src.analysis import BoardUtils
from src.analysis.Technique import NakedSingle
from src.core.BoardState import BoardState
from src.core.Cell import Cell
import random

def createEmptyBoardState() -> BoardState:
    board: list[list[Cell]] = []

    for _ in range(0, 9):
        row = [Cell(None, True) for _ in range(9)]
        board.append(row)

    return BoardState(board)


def createRandomBoardState() -> BoardState:
    state = createEmptyBoardState()

    for _ in range(0, 81):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        value = random.randint(1, 9)

        state.getCell(row, col).setValue(value)

    return state

state = createEmptyBoardState()
assert BoardUtils.getAllCandidates(state) == [[[1,2,3,4,5,6,7,8,9] for _ in range(9)] for _ in range(9)]

while NakedSingle.findAvailable(state) == []:
    state = createRandomBoardState()
print(state)
print(NakedSingle.findAvailable(state))