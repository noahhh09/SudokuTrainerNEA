from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.explanation.Step import Step


class TechniqueExplanation:
    def __init__(self, technique: Technique, board: BoardState):
        self.technique = technique
        self.index = 0
        self.steps: list[Step] = self.getSteps(board)

    def getSteps(self, board: BoardState) -> list[Step]:
        raise NotImplementedError()

    def getPrevious(self):
        self.index = max(0, self.index - 1)
        return self.steps[self.index]

    def getCurrent(self):
        return self.steps[self.index]

    def getNext(self):
        self.index = min(self.index + 1, len(self.steps) - 1)
        return self.steps[self.index]