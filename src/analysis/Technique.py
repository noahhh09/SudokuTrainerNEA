from src.analysis.Unit import Unit, UnitType

from . import BoardUtils

from ..core.Cell import Cell
from ..core.Move import Move, ValueChangeMove
from ..core.BoardState import BoardState

class Technique:
    displayName: str = ""
    description: str = ""

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
                    found.append(NakedSingle([ValueChangeMove(i, j, None, list(candidates)[0])]))

        return found


class HiddenSingle(Technique):
    displayName = "Hidden Single"
    description = "A simple technique where a candidate only appears in one cell."

    def __init__(self, moves: list[Move], unit: Unit) -> None:
        self.unit = unit
        super().__init__(moves)

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        found: list[Technique] = []

        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidateState)

        for unit in units:
            hiddenSingles = HiddenSingle._findHiddenSinglesInUnit(unit)
            for digit, index in hiddenSingles.items():
                row, col = unit.getBoardPosition(index)
                tech = HiddenSingle([ValueChangeMove(row, col, None, digit)], unit)
                found.append(tech)

        return found # Known "bug": might contain duplicates. Say if a block and a column share a hidden single. Whatever.

    # Returns the RELATIVE POSITIONS of single occurrences of a candidate DIGIT in a unit.
    # Dict: [digit, position]
    @staticmethod
    def _findHiddenSinglesInUnit(unit: Unit) -> dict[int, int]:
        singleOccurences: dict[int, int] = {}

        for digit in range(1, 10):
            position = None

            for i in range(9):
                candidates = unit.cells[i].getEffectiveCandidates()
                if digit in candidates:
                    if position is None:
                        position = i
                    else:
                        position = None
                        break # Since this means it's repeated..

            if position is not None and len(unit.cells[position].getEffectiveCandidates()) > 1: # Avoids naked single detection.
                singleOccurences[digit] = position

        return singleOccurences