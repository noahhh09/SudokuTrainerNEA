from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit
from src.core.BoardState import BoardState
from src.core.Move import Move, ValueChangeMove


class HiddenSingle(Technique):
    displayName = "Hidden Single"
    description = "A simple technique where a candidate only appears in one cell."

    def __init__(self, moves: list[Move], causalUnit: Unit, pos: tuple[int, int], digit: int) -> None:
        super().__init__(moves)
        self.causalUnit = causalUnit
        self.pos = pos
        self.digit = digit

    def identity(self) -> str:
        return f"{self.__class__.__name__};{self.causalUnit};{self.pos};{self.digit}"

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        found: list[Technique] = []

        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidateState)

        for unit in units:
            hiddenSingles = HiddenSingle._findHiddenSinglesInUnit(unit)
            for digit, index in hiddenSingles.items():
                row, col = unit.getBoardPosition(index)
                tech = HiddenSingle([ValueChangeMove(row, col, digit)], unit, (row, col), digit)
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

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.causalUnit.unitType.name} {self.causalUnit.unitIndex} {self.moves})"