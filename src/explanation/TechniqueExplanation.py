from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.core.Stack import Stack
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

    def getActiveStack(self) -> Stack: # Allows stacked moves to be properly undone. For example, if a highlight overrides a stack - it wouldn't normaly be fixed when undoing. This just reapplies everything from the stacked moves, in its original order.
        stack = Stack()
        localIndex = self.index - (0 if self.steps[self.index].stackable else 1) # Make it so that if the current move is stackable, that that doesn't get overrided too.
        while localIndex > 0 and self.steps[localIndex].stackable:
            stack.push(self.steps[localIndex])
            localIndex -= 1

        return stack

    def getCurrent(self):
        return self.steps[self.index]

    def getNext(self):
        self.index = min(self.index + 1, len(self.steps) - 1)
        return self.steps[self.index]