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
    @classmethod # ChatGPT made me aware of the @classmethod decorator, but I researched it after the fact and deduced it was a good idea to pass up on. Everything else implemented by self.
    def findAvailable(cls, state: BoardState) -> list[Technique]:
        degree = cls.degree # Allows very easy creation of class-specific types.
        candidateState = BoardUtils.copyAndPopulateCandidates(state)
        units = BoardUtils.getAllUnits(candidateState)

        found: list[Technique] = []

        # Check each unit.
        for unit in units:
            digitOccurrences = BoardUtils.findCandidateDigitOccurrences(unit, upperBound=degree)

            for combo in itertools.combinations(digitOccurrences.items(), degree):
                union: set[int] = set()

                for digit, occurrences in combo:
                    union.update(occurrences)

                if len(union) != degree:
                    continue

                # Almost there - we now just want to check if this hidden group is formed of lower degree hidden groups, or wether it is unique.
                valid = True
                for i in range(1, degree): # This won't cause degree 1 searches to eliminate themselves, since the bounds would be (1,1) and no iteration would occur.
                    for subCombo in itertools.combinations(combo, i):
                        subUnion: set[int] = set()

                        for digit, occurrences in subCombo:
                            subUnion.update(occurrences)

                        if len(subUnion) == i:
                            # Discard.
                            valid = False
                            break

                    if not valid:
                        break

                if not valid:
                    continue

                # We have found a hidden group.
                # Now verify that moves can be made as a result, and create the technique instance:

                moves = []
                digits = {digit for digit, _ in combo}

                for position in union:
                    row, col = unit.getBoardPosition(position)
                    cell = unit.cells[position]
                    toRemove = cell.getEffectiveCandidates() - digits

                    for digit in toRemove:
                        elim = EliminationChangeMove(row, col, digit, True)
                        moves.append(elim)

                if len(moves) > 0:
                    tech = cls(moves, unit, digits, union)
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