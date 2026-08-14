from .BoardState import BoardState


class Technique:
    def checkIfAvailable(self, state: BoardState) -> bool:
        raise NotImplementedError


class NakedSingle(Technique):
    def checkIfAvailable(self, state: BoardState) -> bool:
        candidates = state.getAllCandidates()

        found = False

        for i in range(9):
            for j in range(9):
                if len(candidates[i][j]) == 1:
                    print(f"Found naked single at {i}, {j} for value {candidates[i][j][0]}")
                    found = True

        return found