import itertools

from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit
from src.core.BoardState import BoardState
from src.core.Move import EliminationChangeMove, Move

# NOTE: Works for hidden groups between degree 2 and 9.
class HiddenGroup(Technique):
    displayName = "Hidden Group"
    description = "When two or more candidates only appear in that number of cells in a unit."
    degree: int

    def __init__(self, moves: list[Move], unit: Unit, digits: set[int], causalPositions: set[int]) -> None:
        super().__init__(moves)
        self.unit = unit
        self.digits = digits
        self.causalPositions = causalPositions

    def identity(self) -> str:
        return f"{self.__class__.__name__};{self.unit};{self.causalPositions};{self.digits}"

    def getHintData(self) -> dict[str, str]:
        unit = self.unit

        return {
            "Unit": f"{unit.unitType.name} {unit.unitIndex + 1}",
            "Digits": ", ".join(str(digit) for digit in sorted(list(self.digits))),
            "Causal Positions": " ".join(f"{pos[0], pos[1]}" for pos in (unit.getBoardPosition(relPos) for relPos in self.causalPositions)),
        }

    # If exactly n cells in a unit share (each cell doesn't need them all) the same n candidates between them, and no other cells in that unit do, then all other candidates in these cells can be removed.
    # Approach:
    # - Try every combination of n cells. 
    # - Get candidates. 
    # - Calculate union of each pair intersection. 
    # - If len(union) == degree, then check if the intersection with all other cells is empty.
    @classmethod
    def findAvailable(cls, state: BoardState) -> list[Technique]:
        degree = cls.degree # Allows very easy creation of class-specific types.
        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidateState)

        found: list[Technique] = []

        # Check each unit.
        for unit in units:
            cells = enumerate(unit.cells) # Add relative position to each cell so that it can be referred to later.

            for cellCombination in itertools.combinations(cells, degree):
                union: set[int] = set()
                for pair in itertools.combinations(cellCombination, 2):
                    intersection = pair[0][1].getEffectiveCandidates() & pair[1][1].getEffectiveCandidates()
                    union.update(intersection)

                if len(union) < degree:
                    continue

                # Potential hidden group, but we need to check if they don't appear in any other cells, and that all cells in the combo affect the union.
                # We need to check the following:
                # - The number of cells that intersect with this candidates union == degree
                # - Each cell that contributes when intersected with the union is non-zero in length

                valid = True
                for cell in cellCombination: # check all combo cells contribute to union.
                    if len(cell[1].getEffectiveCandidates() & union) == 0:
                        valid = False
                        break

                if not valid:
                    continue

                valid = True
                toRemove: set[int] = set()
                for digit in union:
                    count = 0
                    for cell in unit.cells:
                        if digit in cell.getEffectiveCandidates():
                            count += 1

                    if count != degree:
                        toRemove.add(digit)

                union = union - toRemove
                if len(union) != degree:
                    continue

                # Valid hidden group!
                # Test for candidates to remove.
                
                moves = []
                for relPos, cell in cellCombination:
                    candidatesToEliminate = cell.getEffectiveCandidates() - union
                    for n in candidatesToEliminate:
                        row, col = unit.getBoardPosition(relPos)
                        elim = EliminationChangeMove(row, col, n, True)
                        moves.append(elim)

                if len(moves) > 0:
                    positions = {cell[0] for cell in cellCombination}
                    tech = cls(moves, unit, union, positions)

                    found.append(tech)

        return found

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.unit.unitType.name} {self.unit.unitIndex} POSITIONS{self.causalPositions} DIGITS{self.digits}, {self.moves})"

class HiddenPair(HiddenGroup):
    displayName = "Hidden Pair"
    description = "When two candidates only appear in 2 cells of a unit."
    degree = 2

class HiddenTriple(HiddenGroup):
    displayName = "Hidden Triple"
    description = "When three candidates only appear in 3 cells of a unit."
    degree = 3