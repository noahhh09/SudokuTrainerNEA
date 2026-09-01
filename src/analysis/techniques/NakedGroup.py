import itertools

from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.analysis.Unit import Unit
from src.core.BoardState import BoardState
from src.core.Cell import Cell
from src.core.Move import EliminationChangeMove, Move


class NakedPair(Technique):
    displayName = "Naked Pair"
    description = "A technique where two cells exclusively have the same two candidates remaining."

    def __init__(self, moves: list[Move], unit: Unit, causalPositions: set[int], candidateUnion: set[int]):
        super().__init__(moves)
        self.unit = unit
        self.causalPositions = causalPositions
        self.candidateUnion = candidateUnion

    def identity(self) -> str:
        return f"{self.__class__.__name__};{self.unit};{self.causalPositions};{self.candidateUnion}"

    def getHintData(self) -> dict[str, str]:
        unit = self.unit

        return {
            "Unit": f"{unit.unitType.name} {unit.unitIndex + 1}",
            "Causal Positions": " ".join(f"{pos[0], pos[1]}" for pos in (unit.getBoardPosition(relPos) for relPos in self.causalPositions)),
            "Digits": ", ".join(str(digit) for digit in sorted(list(self.candidateUnion)))
        }

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidatesState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidatesState)

        found: list[Technique] = []

        for unit in units:
            cells = list(enumerate(unit.cells))
            nakedPairs = _findNakedGroups(cells, 2)

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
        return f"{self.__class__.__name__}({self.unit.unitType.name} {self.unit.unitIndex} POSITIONS{self.causalPositions} UNION{self.candidateUnion}, {self.moves})"

class NakedTriple(Technique):
    displayName = "Naked Triple"
    description = "A technique where three cells contain only three mutual candidates between them, allowing candidates to be ruled out in other cells."

    def __init__(self, moves: list[Move], unit: Unit, causalPositions: set[int], candidateUnion: set[int]):
        super().__init__(moves)
        self.unit = unit
        self.causalPositions = causalPositions
        self.candidateUnion = candidateUnion

    def identity(self) -> str:
        return f"{self.__class__.__name__};{self.unit};{self.causalPositions};{self.candidateUnion}"

    def getHintData(self) -> dict[str, str]:
        unit = self.unit

        return {
            "Unit": f"{unit.unitType.name} {unit.unitIndex + 1}",
            "Causal Positions": " ".join(f"{pos[0] + 1, pos[1] + 1}" for pos in (unit.getBoardPosition(relPos) for relPos in self.causalPositions)),
            "Digits": " ".join(str(digit) for digit in sorted(list(self.candidateUnion)))
        }

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        candidatesState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidatesState)

        found: list[Technique] = []

        for unit in units:
            # Iterate through all cell's candidates. If they match, then all other instances of those candidates can be removed from other cells.
            cells = list(enumerate(unit.cells))

            nakedTriples = _findNakedGroups(cells, 3)
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
        return f"{self.__class__.__name__}({self.unit.unitType.name} {self.unit.unitIndex} POSITIONS{self.causalPositions} UNION{self.candidateUnion}, {self.moves})"

# Returns [(relPositions, candidateValues)]
def _findNakedGroups(cells: list[tuple[int, Cell]], size: int) -> list[tuple[list[int], set[int]]]:
    # AI disclosure - this line was partially generated (the range check at the end) by ChatGPT when reviewing my own implementation of this function.
    cells = [(i, cell) for i, cell in cells if 1 <= len(cell.getEffectiveCandidates()) <= size] # Prematurely remove cells that won't contribute to a naked group.

    cellCombinations = itertools.combinations(cells, size)
    results: list[tuple[list[int], set[int]]] = []

    for combo in cellCombinations:
        candidatesUnion: set[int] = set()

        for _, cell in combo:
            candidatesUnion.update(cell.getEffectiveCandidates())

        if len(candidatesUnion) == size:
            # Eliminate sub groups
            if size == 1:
                positions = [cell[0] for cell in combo]
                results.append((positions, candidatesUnion))
                continue

            hasLowerDegree = False
            for n in range(1, size): # Deep recursion is not a good idea, since if a subgroup contains its own subgroup, it will be skipped.
                subGroups = _findNakedGroups(list(combo), n)
                if len(subGroups) > 0:
                    hasLowerDegree = True # Try next combo. This contains a lower degree group.
                    break

            if hasLowerDegree:
                continue

            # Otherwise, len(subGroups) == 0, so this DOES form a part of a naked group!
            positions = [cell[0] for cell in combo]
            results.append((positions, candidatesUnion))
            
    return results