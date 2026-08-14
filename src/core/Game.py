from core.Move import Move
from core.Stack import Stack


class Game:
    def __init__(self, state, undoStack = Stack(), redoStack = Stack(), mistakeCount = 0, hintsUsed = 0, timeElapsed = 0) -> None:
        self.currentState = state
        self.undoStack = undoStack
        self.redoStack = redoStack
        self.mistakeCount = mistakeCount
        self.hintsUsed = hintsUsed
        self.timeElapsed = timeElapsed

    def makeMove(self, move: Move):
        move.apply(self.currentState)
        self.undoStack.push(move)

    def undoLastMove(self):
        if (self.undoStack.isEmpty()):
            return

        move: Move = self.undoStack.pop()

        move.undo(self.currentState)
        self.redoStack.push(move)

    def redoLastMove(self):
        if (self.redoStack.isEmpty()):
            return

        move: Move = self.redoStack.pop()
        self.makeMove(move)