from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit, UnitType
from src.core.BoardState import BoardState
from src.core.Move import EliminationChangeMove, Move

class PointingGroup(Technique):
    displayName = "Pointing Pair/Triple"
    description = "When candidates are confined to a row/column inside a block, so other instances of the candidate in that row or column can be ruled out."

    def __init__(self, moves: list[Move], affectedUnit: Unit, relatedBlockUnit: Unit, groupPositions: set[tuple[int, int]], digit: int, degree: int) -> None:
        super().__init__(moves)
        self.affectedUnit = affectedUnit
        self.relatedBlockUnit = relatedBlockUnit
        self.groupPositions = groupPositions
        self.digit = digit
        self.degree = degree

    # Pointing techniques exist in two forms - pointing pair and pointing triple. Both are very similar.
    # Summary: all instances of a candidate in a block belong to the same, single unit. -> Eliminate all other candidates not in that unit.
    # Strategy:
    # -> get candidates state 
    # -> iterate through blocks 
    #   -> iterate through 1..9
    #       -> find all cells that have that digit as a candidate
    #       -> if exactly 2 or 3 cells do, find union of rows/cols they belong to
    #       -> if len(that) == 1, we have a potential pointing group
    #       -> if any possible eliminations, pointing group!
    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidatesState = BoardUtils.copyAndPopulateCandidates(state)
        found: list[Technique] = []

        for k in range(9):
            block = Unit(UnitType.Block, k, candidatesState.getBlock(k))
            for digit in range(1, 10):
                memberPositions: set[tuple[int, int]] = set()
                memberRows: set[int] = set()
                memberCols: set[int] = set()

                for i, cell in enumerate(block.cells):
                    if digit in cell.getEffectiveCandidates():
                        row, col = block.getBoardPosition(i)
                        memberPositions.add((row, col))
                        memberRows.add(row)
                        memberCols.add(col)

                if len(memberRows) == 1 and len(memberCols) in (2,3):
                    rowIndex = list(memberRows)[0]
                    rowUnit = Unit(UnitType.Row, rowIndex, candidatesState.getRow(rowIndex))

                    foundEliminationPositions: list[int] = []
                    for colIndex, cell in enumerate(rowUnit.cells):
                        if candidatesState.getBlockIndex(rowIndex, colIndex) == k:
                            continue

                        if digit in cell.getEffectiveCandidates():
                            foundEliminationPositions.append(colIndex)

                    if len(foundEliminationPositions) == 0:
                        continue

                    moves: list[Move] = []
                    for colIndex in foundEliminationPositions:
                        move = EliminationChangeMove(rowIndex, colIndex, digit, True)
                        moves.append(move)

                    found.append(PointingGroup(moves, rowUnit, block, memberPositions, digit, len(memberPositions)))

                elif len(memberCols) == 1 and len(memberRows) in (2,3):
                    colIndex = list(memberCols)[0]
                    colUnit = Unit(UnitType.Column, colIndex, candidatesState.getColumn(colIndex))

                    foundEliminationPositions: list[int] = []
                    for rowIndex, cell in enumerate(colUnit.cells):
                        if candidatesState.getBlockIndex(rowIndex, colIndex) == k:
                            continue

                        if digit in cell.getEffectiveCandidates():
                            foundEliminationPositions.append(rowIndex)

                    if len(foundEliminationPositions) == 0:
                        continue

                    moves: list[Move] = []
                    for rowIndex in foundEliminationPositions:
                        move = EliminationChangeMove(rowIndex, colIndex, digit, True)
                        moves.append(move)

                    found.append(PointingGroup(moves, colUnit, block, memberPositions, digit, len(memberPositions)))

        return found

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(DEGREE {self.degree} DIGIT {self.digit} BY {self.relatedBlockUnit.unitType.name} {self.relatedBlockUnit.unitIndex} AFFECTS {self.affectedUnit.unitType.name} {self.affectedUnit.unitIndex}, {self.moves})"