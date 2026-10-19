from src.analysis.techniques.HiddenGroup import HiddenGroup
from src.core.BoardState import BoardState
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class HiddenGroupExplanation(TechniqueExplanation):
    def __init__(self, technique: HiddenGroup, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        digitsString = self._getDigitsString(self.technique.digits)
        degree = self.technique.degree

        return [
            ShowText(f"A {self.technique.displayName} is when {degree} candidates are shared across {degree} cells in a unit, meaning other candidates in those cells can be eliminated."),
            HighlightCells(f"Let's pay attention to the highlighted unit, {self.technique.unit.readableStr()}.", self.technique.unit, stackable=True),
            PopulateLogicalCandidatesInCells(f"The possible candidates for each cell in the unit have been populated on the left. What might you be able to notice about the {digitsString} digits?", self.technique.unit, stackable=True),
            ShowText(f"Did you notice how the candidates for the {digitsString} digits appear in exactly {degree} positions? What would this mean for the other candidates in those cells?"),
            ApplyMoves(f"This means that all candidates in these cells that are NOT {digitsString} can be eliminated from these cells.", self.technique.moves)
        ]