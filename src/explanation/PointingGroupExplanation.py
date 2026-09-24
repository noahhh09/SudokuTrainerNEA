from src.analysis.techniques.PointingGroup import PointingGroup
from src.core.BoardState import BoardState
from src.core.Move import CandidateChangeMove
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class PointingGroupExplanation(TechniqueExplanation):
    def __init__(self, technique: PointingGroup, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        digit = self.technique.digit
        affectedType = self.technique.affectedUnit.unitType.name

        return [
            ShowText("A pointing group is when candidates are confined to a row/column inside a block, and so other instances of the candidate in that row or column can be ruled out."),
            HighlightCells(f"Where can the digit {digit} be placed in the highlighted block?", self.technique.causalBlockUnit),
            Steps([
                ApplyMoves("", [CandidateChangeMove(row, col, candidateNumber=digit, add=True) for row, col in self.technique.causalPositions]),
                HighlightCells(
                    f"Notice how the digit {digit} can only be placed in these cells, and how these cells share the same {affectedType}?",
                    list(self.technique.causalPositions)
                )
            ]),
            Steps([
                PopulateLogicalCandidatesInCells(
                    f"Since we know that the digit {digit} has to appear inside this block once, and it only appears in this {affectedType}, we can eliminate all other instances of the candidate {digit} from the {affectedType}.",
                    self.technique.affectedUnit
                ),
                ApplyMoves("", self.technique.moves) # TODO: Make this look nicer.
            ]),
            Steps([
                ApplyMoves("", [CandidateChangeMove(row, col, candidateNumber=digit, add=True) for row, col in self.technique.causalPositions]),
                HighlightCells(
                    f"A good way to find pointing groups is by paying attention to where each candidate digit can be placed in each block.",
                    list(self.technique.causalPositions)
                )
            ])
        ]