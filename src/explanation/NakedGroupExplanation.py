from src.analysis.techniques.NakedGroup import NakedGroup
from src.core.BoardState import BoardState
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class NakedGroupExplanation(TechniqueExplanation):
    def __init__(self, technique: NakedGroup, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        digits = self.technique.candidateUnion
        digitsString = self._getDigitsString(digits)

        causalBoardPositions = [self.technique.unit.getBoardPosition(i) for i in self.technique.causalPositions]

        return [
            ShowText("A Naked group technqiue is one where a number of candidates both appear exclusively in the same number of cells, allowing these candidate digits to be eliminated from other cells."),
            HighlightCells(f"Lets pay attention to this unit, {self.technique.unit.readableStr()}. What candidates could fill each cell?", self.technique.unit),
            PopulateLogicalCandidatesInCells(f"What do you notice about the {digitsString} digits?", self.technique.unit, stackable=True),
            HighlightCells(f"Each of the highlighted cells must be either {digitsString.replace("and", "or")}, since they are the only {len(digits)} candidates in these {len(digits)} cells.", causalBoardPositions, stackable=True),
            ApplyMoves(f"This means we can eliminate all instances of {digitsString} elsewhere in the unit, since they must occur in these {len(digits)} cells.", self.technique.moves),
            Steps([
                PopulateAllLogicalCandidates("The best way to find naked group techniques is to pencil in all possible candidates and spot any groups of 2, or 3, or more of the same candidate across those cells."),
                HighlightCells("", causalBoardPositions)
            ])
        ]

    # Lets look at this unit.
    # lets popualte every candidate for the cells in that unit
    # notice how these X cells are the only spots where these X digits appear?
    # that means they *must* be in any of those cells, so any other candidates in those cells can be eliminated.