from src.analysis.techniques.HiddenSingle import HiddenSingle
from src.core.BoardState import BoardState
from src.explanation.Step import *
from src.explanation.TechniqueExplanation import TechniqueExplanation


class HiddenSingleExplanation(TechniqueExplanation):
    def __init__(self, technique: HiddenSingle, board: BoardState):
        self.technique = technique
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        digit = self.technique.digit

        positionsOfThisDigit = [(i, j) for i in range(9) for j in range(9) if board.getCell(i, j).getValue() == digit]
        units = []
        memberUnitHighlights: list[Steps] = []
        for row, col in positionsOfThisDigit:
            memberUnits = BoardUtils.getMemberUnits(board, row, col)
            group: list[Step] = []

            for unit in memberUnits:
                units.append(unit)

                group.append(
                    HighlightCells(f"Let's focus on the digit {digit}, and eliminate every unit that contains the digit {digit}.", unit, "#ff8e8e")
                )

            memberUnitHighlights.append(Steps(group, stackable=True))

        unitPositions = [unit.getBoardPosition(i) for i in range(9) for unit in units]

        return [
            ShowText("A Hidden Single is when a single candidate appears just once across an entire unit."),
            HighlightCells(f"Lets pay attention to the unit highlighted. Try to figure out which cells could possibly have the digit {digit}. In other words, where can the digit 6 be placed in this unit?", self.technique.causalUnit),
            Steps([
                PopulateLogicalCandidatesInCells("", self.technique.causalUnit),
                HighlightCells(f"Notice how the digit {digit} can only be placed inside one cell in this unit?", [self.technique.pos])
            ]),
            ApplyMove(
                f"Since every unit must have at least one instance of each number, and the digit {digit} only appears in this one cell in the unit, it must be placed here. As a result, we can change the value of this cell to {digit}.",
                ValueChangeMove(*self.technique.pos, digit)
            ),
            # Finding Hidden Singles
            HighlightCells(f"Finding Hidden Singles: Cross-hatching - A nice way of finding Hidden Singles is by focusing on all the instances of a single digit in a board. Let's focus on the digit {digit}, and eliminate every unit that contains the digit {digit}.", positionsOfThisDigit, stackable=True),
            *memberUnitHighlights,
            ShowText(f"Notice anything special in {self.technique.causalUnit.readableStr()} after 'cross-hatching' the digit {digit}?"),
            Steps([
                ApplyMove(
                    f"Did you notice how only one empty cell remained in {self.technique.causalUnit.readableStr()}? That means that this cell must be the digit we cross-hatched ({digit}), a case of a Hidden Single.",
                    ValueChangeMove(*self.technique.pos, digit)
                ),
                HighlightCells("", unitPositions, "#ff8e8e")
            ])

        ]