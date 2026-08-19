from enum import Enum

from ..core.Cell import Cell
from ..core.BoardState import BoardState

# Enums just help with data integrity I think.
class UnitType(Enum):
    ROW = "row"
    COLUMN = "column"
    BLOCK = "block"

class Contradiction:
    # A 'unit' is defined as an array of 9 cells. It's an instance of a row, column, or block.
    def __init__(self, value: int, unitType: UnitType, unitIndex: int, positionsInvolved: list[tuple[int, int]]) -> None:
        self.value = value
        self.unitType = unitType
        self.unitIndex = unitIndex
        self.cellsInvolved = positionsInvolved

    def __str__(self) -> str:
        return f"Contradiction(value:{self.value}, type:{self.unitType}, unitIndex: {self.unitIndex}, cells:{self.cellsInvolved})"

    def __repr__(self) -> str:
        return self.__str__()

def detectContradictions(state: BoardState) -> list[Contradiction]:
    allContradictions: list[Contradiction] = []

    # Check rows
    for i in range(0, 9):
        unit = state.getRow(i)
        duplicates = _getDuplicatesInUnit(unit)

        for value, positions in duplicates.items():
            contra = Contradiction(value, UnitType.ROW, i, [(i, x) for x in positions])
            allContradictions.append(contra)

    # Check cols
    for j in range(0, 9):
        unit = state.getColumn(j)
        duplicates = _getDuplicatesInUnit(unit)

        for value, positions in duplicates.items():
            contra = Contradiction(value, UnitType.COLUMN, j, [(x, j) for x in positions])
            allContradictions.append(contra)

    # Check blocks
    for k in range(0, 9):
        unit = state.getBlock(k)
        duplicates = _getDuplicatesInUnit(unit)

        for value, positions in duplicates.items():
            contra = Contradiction(value, UnitType.BLOCK, k, [state.getPositionInBlock(k, x) for x in positions])
            allContradictions.append(contra)

    return allContradictions
    

def _getDuplicatesInUnit(unit: list[Cell]) -> dict[int, list[int]]:
    instances: dict[int, list[int]] = {} # Stores positional index of instances of each unique digit.

    for i in range(9):
        value = unit[i].getValue() 

        if value is not None:
            instances[value] = instances.get(value, []) + [i]
           
    filtered = {value: positions for value, positions in instances.items() if len(positions) > 1} # Filters only such that there are actual contradictions.
    return filtered