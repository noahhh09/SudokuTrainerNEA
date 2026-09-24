from src.analysis.techniques.NakedSingle import NakedSingle
from src.core.BoardState import BoardState
from src.core.Move import ValueChangeMove
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class NakedSingleExplanation(TechniqueExplanation):
    def __init__(self, technique: NakedSingle, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        digit = self.technique.digit

        units = BoardUtils.getMemberUnits(board, *self.technique.pos)
        positions = [[unit.getBoardPosition(i) for i in range(9)] for unit in units]
        positions = positions[0] + positions[1] + positions[2]

        allInstances = NakedSingle.findAvailable(board) 
        otherNakedSinglePositions: list[tuple[int, int]] = []
        for instance in allInstances:
            # Type hinting sucks
            if type(instance) is not NakedSingle:
                continue

            otherNakedSinglePositions.append(instance.pos)

        return [
            ShowText("A Naked Single occurs when a cell has only one single candidate remaining, meaning it has to be that value."),
            HighlightCells("Look at this position.", [self.technique.pos]),
            Steps([
                HighlightCells("", positions),
                HighlightCells(f"Look at the wider units this cell is a part of. Notice how the digits 1-9 except for {digit} all appear somewhere in these units. What might this mean for this cell?", [self.technique.pos], "yellow")
            ]),
            PopulateCandidatesInCells(f"That means that this cell can only have the digit {digit} as a candidate.", [self.technique.pos]),
            UpdateCellValue(f"Since the digit {digit} is the only candidate, this number must be in this cell.", *self.technique.pos, digit),
            Steps([
                UpdateCellValue("", *self.technique.pos, None),
                PopulateAllCandidates(""),
                HighlightCells("Finding Naked Singles: Naked Singles are easy to spot once you are sure of all the candidates in one cell.", otherNakedSinglePositions),
            ])
        ]

