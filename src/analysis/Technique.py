from . import BoardUtils

from ..core.Move import Move, ValueChangeMove
from ..core.BoardState import BoardState


class Technique:
    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()


class NakedSingle(Technique):
    def __init__(self, moves: list[Move]) -> None:
        super().__init__(moves)

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidates = BoardUtils.getAllCandidates(state)

        found: list[Technique] = []

        for i in range(9):
            for j in range(9):
                if len(candidates[i][j]) == 1:
                    found.append(NakedSingle([ValueChangeMove(i, j, 0, candidates[i][j][0])]))

        return found

    def __str__(self) -> str:
        return f"NakedSingle({self.moves[0]})"
