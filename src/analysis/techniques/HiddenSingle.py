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

    def getHintData(self) -> dict[str, str]:
        row, col = self.pos

        return {
            "Digit": str(self.digit),
            "Cell Position": f"Row {row + 1}, Column {col + 1}",
            "Causal Unit": f"{self.causalUnit.unitType.name} {self.causalUnit.unitIndex + 1}"
        }

    @classmethod
    def findAvailable(cls, state: BoardState) -> list[Technique]:
        found: list[Technique] = []

        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidateState)

        for unit in units:
            for digit in range(1, 10):
                index = None

                for i in range(9):
                    candidates = unit.cells[i].getEffectiveCandidates()

                    if digit in candidates:
                        if index is None:
                            index = i
                        else:
                            index = None # Because this would only happen if position has been updated before, hence this is NOT a Hidden Single.
                            break

                if index is not None and len(unit.cells[index].getEffectiveCandidates()) > 1: # Second check ensures no naked singles are detected.
                    row, col = unit.getBoardPosition(index)
                    move = ValueChangeMove(row, col, digit)
                    technique = HiddenSingle([move], unit, (row, col), digit)
                    found.append(technique)

        return found

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.causalUnit.unitType.name} {self.causalUnit.unitIndex} {self.moves})"