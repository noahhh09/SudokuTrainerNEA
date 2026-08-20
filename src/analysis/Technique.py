from . import BoardUtils

from ..core.Cell import Cell
from ..core.Move import Move, ValueChangeMove
from ..core.BoardState import BoardState


class Technique:
    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.moves})"

    def __repr__(self) -> str:
        return self.__str__()


class NakedSingle(Technique):
    def __init__(self, moves: list[Move]) -> None:
        super().__init__(moves)

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidateState = BoardUtils.copyAndPopulateCandidates(state)

        found: list[Technique] = []

        for i in range(9):
            for j in range(9):
                candidates = candidateState.getCell(i, j).getCandidates()
                if len(candidates) == 1:
                    found.append(NakedSingle([ValueChangeMove(i, j, None, list(candidates)[0])]))

        return found


class HiddenSingle(Technique):
    def __init__(self, moves: list[Move]) -> None:
        super().__init__(moves)

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        found: list[Technique] = []

        for i in range(9):
            print("ROW", i)
            unit = candidateState.getRow(i)
            hiddenSingles = HiddenSingle._findHiddenSinglesInUnit(unit)
            for digit, col in hiddenSingles.items():
                tech = HiddenSingle([ValueChangeMove(i, col, None, digit)])
                found.append(tech)

        for j in range(9):
            print("COL", j)
            unit = candidateState.getColumn(j)
            hiddenSingles = HiddenSingle._findHiddenSinglesInUnit(unit)
            for digit, row in hiddenSingles.items():
                print("COL", j, digit, row)
                tech = HiddenSingle([ValueChangeMove(row, j, None, digit)])
                found.append(tech)

        for k in range(9):
            print("BLK", k)
            unit = candidateState.getBlock(k)
            hiddenSingles = HiddenSingle._findHiddenSinglesInUnit(unit)
            for digit, index in hiddenSingles.items():
                print("BLK", k, digit, index)
                row, col = candidateState.getPositionInBlock(k, index)
                tech = HiddenSingle([ValueChangeMove(row, col, None, digit)])
                found.append(tech)

        return found # Known "bug": might contain duplicates. Say if a block and a column share a hidden single. Whatever.

    # Returns the RELATIVE POSITIONS of single occurrences of a candidate DIGIT in a unit.
    # Dict: [digit, position]
    @staticmethod
    def _findHiddenSinglesInUnit(unit: list[Cell]) -> dict[int, int]:
        singleOccurences: dict[int, int] = {}

        for digit in range(1, 10):
            position = None

            for i in range(9):
                candidates = unit[i].getCandidates()
                print("--CHK", i, candidates)
                if digit in candidates:
                    if position is None:
                        print("Found", digit, i)
                        position = i
                    else:
                        print("Rejecting", digit, i)
                        position = None
                        break # Since this means it's repeated..

            if position is not None and len(unit[position].getCandidates()) > 1: # Avoids naked single detection.
                singleOccurences[digit] = position

        return singleOccurences