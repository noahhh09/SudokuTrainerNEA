from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.core.Move import Move, ValueChangeMove


class NakedSingle(Technique):
    displayName = "Naked Single"
    description = "A simple technique where a cell has only one candidate remaining."

    def __init__(self, moves: list[Move]) -> None:
        super().__init__(moves)

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidateState = BoardUtils.copyAndPopulateCandidates(state)

        found: list[Technique] = []

        for i in range(9):
            for j in range(9):
                candidates = candidateState.getCell(i, j).getEffectiveCandidates()
                if len(candidates) == 1:
                    found.append(NakedSingle([ValueChangeMove(i, j, list(candidates)[0])]))

        return found