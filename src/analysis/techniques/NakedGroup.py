import itertools

from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit, UnitType
from src.core.BoardState import BoardState
from src.core.Cell import Cell
from src.core.Move import EliminationChangeMove, Move


class NakedPair(Technique):
    displayName = "Naked Pair"
    description = "A technique where two cells exclusively have the same two candidates remaining."

    def __init__(self, moves: list[Move], unit: Unit):
        super().__init__(moves)
        self.unit = unit

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidatesState = BoardUtils.copyAndPopulateCandidates(state) # TODO: Change to preserve eliminations
        units = BoardUtils.getAllUnits(candidatesState)

        found: list[Technique] = []

        for unit in units:
            # Iterate through all cell's candidates. If they match, then all other instances of those candidates can be removed from other cells.

            nakedPairs = _findNakedGroups(unit, 2)
            for positions, union in nakedPairs:
                moves: list[Move] = []

                positionsToCheck = set(range(9)) - set(positions)
            
                for relPos in positionsToCheck:
                    candidatesToEliminate = unit.cells[relPos].getEffectiveCandidates().intersection(union)
    
                    if candidatesToEliminate:
                        row, col = unit.getBoardPosition(relPos)
                        for n in candidatesToEliminate:
                            elim = EliminationChangeMove(row, col, n, True)
                            moves.append(elim)

                if len(moves) != 0:
                    tech = NakedPair(moves, unit)
                    found.append(tech)

        return found

class NakedTriple(Technique):
    displayName = "Naked Triple"
    description = "A technique where three cells contain only three mutual candidates between them, allowing candidates to be ruled out in other cells."

    def __init__(self, moves: list[Move], unit: Unit):
        super().__init__(moves)
        self.unit = unit

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidatesState = BoardUtils.copyAndPopulateCandidates(state) # TODO: Change to preserve eliminations
        units = BoardUtils.getAllUnits(candidatesState)

        found: list[Technique] = []

        for unit in units:
            # Iterate through all cell's candidates. If they match, then all other instances of those candidates can be removed from other cells.

            nakedTriples = _findNakedGroups(unit, 3)
            for positions, union in nakedTriples:
                moves: list[Move] = []

                positionsToCheck = set(range(9)) - set(positions)
            
                for relPos in positionsToCheck:
                    candidatesToEliminate = unit.cells[relPos].getEffectiveCandidates().intersection(union)
    
                    if candidatesToEliminate:
                        row, col = unit.getBoardPosition(relPos)
                        for n in candidatesToEliminate:
                            elim = EliminationChangeMove(row, col, n, True)
                            moves.append(elim)

                if len(moves) != 0:
                    tech = NakedTriple(moves, unit)
                    found.append(tech)

        return found

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.unit.unitType.name} {self.unit.unitIndex}, {self.moves})"

# Returns [(relPositions, candidateValues)]
def _findNakedGroups(unit: Unit, size: int) -> list[tuple[list[int], set[int]]]:
    cells = list(enumerate(unit.cells))
    
    cellCombinations = itertools.combinations(cells, size)
    foundGroups = []

    for combo in cellCombinations:
        union: set[int] = set()
        for _, cell in combo:
            if len(cell.getEffectiveCandidates()) != 0:
                union.update(cell.getEffectiveCandidates())

        if len(union) == size:
            legal = True
            for _, cell in combo:
                if legal:
                    legal = 1 < len(cell.getEffectiveCandidates()) <= size

            if not legal:
                continue

            # union contains all candidates that make up the naked group.
            # And all cells in combo are the cells that make it up.

            positions = [x[0] for x in combo]
            foundGroups.append((positions, union))

    return foundGroups
