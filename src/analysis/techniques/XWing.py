import time

from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit, UnitType
from src.core.BoardState import BoardState
from src.core.Move import EliminationChangeMove, Move


class XWing(Technique):
    displayName = "X-Wing"
    description = "When a candidate appears twice in two rows, and appears in the same columns within those rows. Or vice versa."

    def __init__(self, moves: list[Move], baseDirection: UnitType, baseUnits: list[Unit], coverUnits: list[Unit], digit: int) -> None:
        super().__init__(moves)
        self.baseDirection = baseDirection
        self.baseUnits = baseUnits
        self.coverUnits = coverUnits
        self.digit = digit

    def identity(self) -> str:
        return f"{self.__class__.__name__};{self.digit};{self.baseUnits};{self.coverUnits}"

    def getHintData(self) -> dict[str, str]:
        return {
            "Digit": str(self.digit),
            "Base Unit Type": self.baseDirection.name,
            "Base Units": ", ".join([unit.readableStr() for unit in self.baseUnits]),
            "Cover Units": ", ".join([unit.readableStr() for unit in self.coverUnits])
        }

    @classmethod
    def findAvailable(cls, state: BoardState) -> list[Technique]:
        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        found = []

        rowUnits = BoardUtils.getUnitsOfKind(candidateState, UnitType.Row)
        colUnits = BoardUtils.getUnitsOfKind(candidateState, UnitType.Column)

        occurrencesByRow: list[dict[int, set[int]]] = []
        occurrencesByCol: list[dict[int, set[int]]] = []

        for row in rowUnits:
            occurrencesByRow.append(BoardUtils.findCandidateDigitOccurrences(row))

        for col in colUnits:
            occurrencesByCol.append(BoardUtils.findCandidateDigitOccurrences(col))

        for i, row in enumerate(occurrencesByRow):
            for digit, occurrences in row.items():
                if len(occurrences) != 2:
                    continue # Definitely not gonna form an X-Wing

                for j in range(i + 1, 9):          
                    if digit not in occurrencesByRow[j]:
                        continue

                    if occurrencesByRow[j][digit] == occurrences:
                        # We have an X-Wing pattern. We need to check if consequential moves can occur in each column.
                        positionsToRemove: list[tuple[int, int]] = []
                        for column in occurrences:
                            toRemove = occurrencesByCol[column][digit] - {i,j}
                            positions = [(row, column) for row in toRemove]
                            positionsToRemove += positions

                        if len(positionsToRemove) > 0:
                            moves = []
                            for row, col in positionsToRemove:
                                move = EliminationChangeMove(row, col, digit, True)
                                moves.append(move)

                            occurrenceUnits = []
                            for occ in occurrences:
                                occurrenceUnits.append(colUnits[occ])

                            tech = XWing(moves, UnitType.Row, [rowUnits[i], rowUnits[j]], occurrenceUnits, digit)
                            found.append(tech)

        for i, col in enumerate(occurrencesByCol):
            for digit, occurrences in col.items():
                if len(occurrences) != 2:
                    continue # Definitely not gonna form an X-Wing

                for j in range(i + 1, 9):          
                    if digit not in occurrencesByCol[j]:
                        continue

                    if occurrencesByCol[j][digit] == occurrences:
                        # We have an X-Wing pattern. We need to check if consequential moves can occur in each column.
                        positionsToRemove: list[tuple[int, int]] = []
                        for row in occurrences:
                            toRemove = occurrencesByRow[row][digit] - {i,j}
                            positions = [(row, column) for column in toRemove]
                            positionsToRemove += positions

                        if len(positionsToRemove) > 0:
                            moves = []
                            for row, col in positionsToRemove:
                                move = EliminationChangeMove(row, col, digit, True)
                                moves.append(move)

                            occurrenceUnits = []
                            for occ in occurrences:
                                occurrenceUnits.append(rowUnits[occ])

                            tech = XWing(moves, UnitType.Column, [colUnits[i], colUnits[j]], occurrenceUnits, digit)
                            found.append(tech)

        return found

    