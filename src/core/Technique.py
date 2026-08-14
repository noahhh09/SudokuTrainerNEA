from .Move import Move, ValueChangeMove
from .BoardState import BoardState


class Technique:
    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        raise NotImplementedError


class NakedSingle(Technique):
    def __init__(self, moves: list[Move]) -> None:
        super().__init__(moves)

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidates = state.getAllCandidates()

        found: list[Technique] = []

        for i in range(9):
            for j in range(9):
                if len(candidates[i][j]) == 1:
                    found.append(NakedSingle([ValueChangeMove(i, j, 0, candidates[i][j][0])]))

        return found