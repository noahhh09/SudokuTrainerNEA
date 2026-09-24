from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.explanation.Step import Step
from src.explanation.TechniqueExplanation import TechniqueExplanation


class HiddenSingleExplanation(TechniqueExplanation):
    def __init__(self, technique: Technique, board: BoardState):
        super().__init__(technique, board)

    def getSteps(self, board: BoardState) -> list[Step]:
        return []