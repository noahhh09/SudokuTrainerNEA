from .Move import Move
from .Stack import Stack
from .BoardState import BoardState

class Game:
    def __init__(self, state: BoardState, undoStack = Stack(), redoStack = Stack(), mistakeCount = 0, hintsUsed = 0, timeElapsed = 0) -> None:
        self.boardState = state
        self.undoStack = undoStack
        self.redoStack = redoStack
        self.mistakeCount = mistakeCount
        self.hintsUsed = hintsUsed
        self.timeElapsed = timeElapsed

    def makeMove(self, move: Move):
        move.apply(self.boardState)
        self.undoStack.push(move)
        self.redoStack.clear()

    def undoLastMove(self):
        if (self.undoStack.isEmpty()):
            return

        move: Move = self.undoStack.pop()

        move.undo(self.boardState)
        self.redoStack.push(move)

    def redoLastMove(self):
        if (self.redoStack.isEmpty()):
            return

        move: Move = self.redoStack.pop()
        move.apply(self.boardState)
        self.undoStack.push(move)