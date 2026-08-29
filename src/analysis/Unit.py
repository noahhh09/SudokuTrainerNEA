# Enums just help with data integrity I think.
from enum import Enum

from src.core.Cell import Cell


class UnitType(Enum):
    Row = "row"
    Column = "column"
    Block = "block"


class Unit:
    def __init__(self, unitType: UnitType, unitIndex: int, cells: list[Cell]):
        self.unitType = unitType
        self.unitIndex = unitIndex
        self.cells = cells

    def getBoardPosition(self, index: int) -> tuple[int, int]:
        match self.unitType:
            case UnitType.Row:
                return (self.unitIndex, index)
            case UnitType.Column:
                return (index, self.unitIndex)
            case UnitType.Block:
                row = (self.unitIndex // 3) * 3 + (index // 3)
                col = (self.unitIndex % 3) * 3 + (index % 3)
                
                return (row, col)
