import itertools

from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit
from src.core.BoardState import BoardState
from src.core.Move import EliminationChangeMove, Move


class NakedPair(Technique):
    displayName = "Naked Pair"
    description = "A technique where two cells exclusively have the same two candidates remaining."

    def __init__(self, moves: list[Move], unit: Unit, group: set[int], union: set[int]):
        super().__init__(moves)
        self.unit = unit
        self.groupPositions = group
        self.union = union

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
                    tech = NakedPair(moves, unit, set(positions), union)
                    found.append(tech)

        return found

    # Used for debugging.
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.unit.unitType.name} {self.unit.unitIndex} POSITIONS{self.groupPositions} UNION{self.union}, {self.moves})"

class NakedTriple(Technique):
    displayName = "Naked Triple"
    description = "A technique where three cells contain only three mutual candidates between them, allowing candidates to be ruled out in other cells."

    def __init__(self, moves: list[Move], unit: Unit, groupPositions: set[int], union: set[int]):
        super().__init__(moves)
        self.unit = unit
        self.groupPositions = groupPositions
        self.union = union

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidatesState = BoardUtils.copyAndPopulateCandidates(state)
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

                    if len(candidatesToEliminate) > 0:
                        row, col = unit.getBoardPosition(relPos)
                        for n in candidatesToEliminate:
                            elim = EliminationChangeMove(row, col, n, True)
                            moves.append(elim)

                if len(moves) != 0:
                    tech = NakedTriple(moves, unit, set(positions), union)
                    found.append(tech)

        return found

    # Used for debugging.
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.unit.unitType.name} {self.unit.unitIndex} POSITIONS{self.groupPositions} UNION{self.union}, {self.moves})"

# Returns [(relPositions, candidateValues)]
# TODO - Remove lower degree naked groups from this set.
def _findNakedGroups(unit: Unit, size: int) -> list[tuple[list[int], set[int]]]:
    cells = list(enumerate(unit.cells))
    cells = [(i, cell) for i, cell in cells if 1 < len(cell.getEffectiveCandidates()) <= size] # Prematurely removes naked singles and cells that won't contribute to a naked pair.
    
    cellCombinations = itertools.combinations(cells, size)
    foundGroups = []

    for combo in cellCombinations:
        union: set[int] = set()
        for _, cell in combo:
            union.update(cell.getEffectiveCandidates())

        if len(union) == size:
            legal = True

            # Determine if there are any naked subset groups.
            for n in range(2, size):
                # Iterate through all combinations of size n inside the combo
                for subset in itertools.combinations(combo, n):
                    subsetUnion: set[int] = set()
                    for _, subCell in subset:
                        subsetUnion.update(subCell.getEffectiveCandidates())
                    
                    if len(subsetUnion) == n:
                        legal = False
                        break

                if not legal:
                    break

            if not legal:
                continue

            # union contains all candidates that make up the naked group.
            # And all cells in combo are the cells that make it up.

            positions = [x[0] for x in combo]
            foundGroups.append((positions, union))

    return foundGroups
