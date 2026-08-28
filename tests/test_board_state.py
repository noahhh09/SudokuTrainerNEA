from src.analysis.techniques.NakedSingle import NakedSingle
from src.core.BoardState import BoardState
from src.core.Cell import Cell
import random

def createEmptyBoardState() -> BoardState:
    board: list[list[Cell]] = []

    for _ in range(0, 9):
        row = [Cell(None, True) for _ in range(9)]
        board.append(row)

    return BoardState(board)


def createRandomBoardState(n: int) -> BoardState:
    state = createEmptyBoardState()

    for _ in range(0, n):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        value = random.randint(1, 9)

        state.getCell(row, col).setValue(value)

    return state

state = createEmptyBoardState()

while NakedSingle.findAvailable(state) == []:
    state = createRandomBoardState(64)
# print(state)
# print(NakedSingle.findAvailable(state))