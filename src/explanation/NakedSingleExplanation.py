from src.analysis.techniques.NakedSingle import NakedSingle
from src.core.BoardState import BoardState
from src.core.Move import EliminationChangeMove, ValueChangeMove
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class NakedSingleExplanation(TechniqueExplanation):
    def __init__(self, technique: NakedSingle, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        digit = self.technique.digit

        units = BoardUtils.getMemberUnits(board, *self.technique.pos)
        memberUnitPositions = [[unit.getBoardPosition(i) for i in range(9)] for unit in units]
        memberUnitPositions = memberUnitPositions[0] + memberUnitPositions[1] + memberUnitPositions[2]

        eliminations: list[Move] = [EliminationChangeMove(*self.technique.pos, x, add=True) for x in ({1,2,3,4,5,6,7,8,9} - {digit})]

        allInstances = NakedSingle.findAvailable(board) 
        otherNakedSinglePositions: list[tuple[int, int]] = []
        for instance in allInstances:
            # Type hinting sucks
            if type(instance) is not NakedSingle:
                continue

            otherNakedSinglePositions.append(instance.pos)
        return [
            ShowText("A Naked Single occurs when a cell has only one single candidate remaining, meaning it has to be that value."),
            HighlightCells("Lets look at this cell.", [self.technique.pos]),
            Steps([
                HighlightCells("", memberUnitPositions),
                HighlightCells(f"Look at the wider units this cell is a part of (as highlighted). Notice how the digits 1-9 except for {digit} all appear at least once in the highlighted units? What might this mean for the candidates in the main cell?", [self.technique.pos], "yellow")
            ]),
            Steps([
                PopulateEveryCandidateNumberInCells("", [self.technique.pos]),
                ApplyMoves("", eliminations),
                HighlightCells(f"In terms of candidates, notice that means that each possible candidate digit apart from {digit} can be eliminated?", [self.technique.pos])
            ]),
            PopulateLogicalCandidatesInCells(f"That means that this cell can only have the digit {digit} as a candidate.", [self.technique.pos]),
            ApplyMove(f"Since the digit {digit} is the only candidate, and this cell will have to be filled, the digit {digit} must be in this cell.", ValueChangeMove(*self.technique.pos, digit)),
            Steps([
                PopulateAllLogicalCandidates(""),
                HighlightCells("Finding Naked Singles: Naked Singles are easy to spot once you are sure of all the candidates in one cell. The cell will simply have one candidate only.", otherNakedSinglePositions),
            ])
        ]

