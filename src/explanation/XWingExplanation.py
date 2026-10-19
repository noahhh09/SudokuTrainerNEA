from src.analysis.techniques.XWing import XWing
from src.core.BoardState import BoardState
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class XWingExplanation(TechniqueExplanation):
    def __init__(self, technique: XWing, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        exampleRowCol = self.technique.baseUnits[0].getBoardPosition(self.technique.coverUnits[0].unitIndex)
        complementaryRowCol = self.technique.baseUnits[1].getBoardPosition(self.technique.coverUnits[1].unitIndex)
        digit = self.technique.digit

        return [
            ShowText("X-Wings are powerful techniques that make use of two parallel 'base units'. When the same candidate appears in both base units, and also in the same complementary unit (e.g. if the base units were rows, then columns), then other instances of the candidate in those complementary units can be eliminated. Let's take a look."),
            Steps([
                PopulateLogicalCandidatesInCells("", self.technique.baseUnits[0]),
                PopulateLogicalCandidatesInCells("", self.technique.baseUnits[1]),
                HighlightCells("", self.technique.baseUnits[0]),
                HighlightCells("", self.technique.baseUnits[1]),
                ShowText(f"Look at the {self.technique.digit} digit in the highlighted units. The possible candidates have already been populated. What do you notice about the positions of the candidates for the {digit} digit inside these units?")
            ], stackable=True),
            Steps([
                HighlightCells("", self.technique.causalPositions, "yellow"),
                ShowText(f"Did you notice how the {digit} digit only appears in {self.technique.coverUnits[0].readableStr()} and {self.technique.coverUnits[1].readableStr()} in BOTH of these units?")
            ], stackable=True),
            ApplyMove(f"Suppose the digit {digit} was added into one of these cells. What affect would this have on the other cells?", ValueChangeMove(*exampleRowCol, digit), stackable=True),
            Steps([
                ApplyMove(f"Since the {digit} digit cannot be in the same row or column, it will always be in the opposite position.", ValueChangeMove(*complementaryRowCol, digit))
            ], stackable=True),
            Steps([
                ApplyMove("", ValueChangeMove(*exampleRowCol, None)),
                ApplyMove("", ValueChangeMove(*complementaryRowCol, None)),
                PopulateLogicalCandidatesInCells("", self.technique.baseUnits[0]),
                PopulateLogicalCandidatesInCells("", self.technique.baseUnits[1]),
                HighlightCells("", self.technique.causalPositions),
                ShowText(f"This means that the {digit} digit must be in one of these two cells inside each {self.technique.baseDirection.name}. What does this mean for other cells in each {self.technique.baseDirection.name}?"),
            ], stackable=True),
            ApplyMoves(f"Since the {digit} digit is locked to these cells, any other instance in each {self.technique.coverUnits[0].unitType.name} can be eliminated.", self.technique.moves, stackable=True),
            Steps([
                PopulateLogicalCandidatesInCells("", self.technique.baseUnits[0]),
                PopulateLogicalCandidatesInCells("", self.technique.baseUnits[1]),
                HighlightCells("", self.technique.baseUnits[0]),
                HighlightCells("", self.technique.baseUnits[1]),
                ShowText(f"Finding X-Wings: X-Wings are most easily found by looking at two parallel units and noticing if any candidates are locked to the same two complementing units.")
            ])
        ]