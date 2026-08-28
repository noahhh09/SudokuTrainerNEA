from src.analysis import BoardUtils
from src.analysis.Unit import Unit, UnitType

from ..core.Cell import Cell
from ..core.BoardState import BoardState


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

    units = BoardUtils.getAllUnits(state)
    for unit in units:
        duplicates = _getDuplicatesInUnit(unit)

        for value, positions in duplicates.items():
            contra = Contradiction(value, unit.unitType, unit.unitIndex, [unit.getBoardPosition(x) for x in positions])
            allContradictions.append(contra)
            
    return allContradictions
    
# Returns a dictionary of values with duplicates in this unit, with the value representing all relative indices of where these contradictions have occurred.
def _getDuplicatesInUnit(unit: Unit) -> dict[int, list[int]]:
    instances: dict[int, list[int]] = {} # Stores positional index of instances of each unique digit.

    for i in range(9):
        value = unit.cells[i].getValue() 

        if value is not None:
            instances[value] = instances.get(value, []) + [i]
           
    filtered = {value: positions for value, positions in instances.items() if len(positions) > 1} # Filters only such that there are actual contradictions.
    return filtered