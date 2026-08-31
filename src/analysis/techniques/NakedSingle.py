from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.core.Move import Move, ValueChangeMove


class NakedSingle(Technique):
    displayName = "Naked Single"
    description = "A simple technique where a cell has only one candidate remaining."

    def __init__(self, moves: list[Move], pos: tuple[int, int], digit: int) -> None:
        super().__init__(moves)
        self.pos = pos
        self.digit = digit

    def identity(self) -> str:
        return f"{self.__class__.__name__};{self.pos}{self.digit}"

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidateState = BoardUtils.copyAndPopulateCandidates(state)

        found: list[Technique] = []

        for i in range(9):
            for j in range(9):
                candidates = candidateState.getCell(i, j).getEffectiveCandidates()
                if len(candidates) == 1:
                    digit = list(candidates)[0]
                    found.append(NakedSingle([ValueChangeMove(i, j, digit)], (i, j), digit))

        return found