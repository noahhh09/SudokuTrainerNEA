import { BoardState } from "./BoardState";
import { Move } from "./Move";
import { Stack } from "./Stack";

export class Game {
    constructor(
        public currentState: BoardState,
        public undoStack: Stack<Move>,
        public redoStack: Stack<Move>,
        public mistakeCount: number,
        public hintsUsed: number,
        public timeElapsed: number
    ) {}

    makeMove(move: Move) {
        move.apply(this.currentState)
        this.undoStack.push(move)
    }

    undoLastMove() {
        if (this.undoStack.isEmpty()) return

        const move = this.undoStack.pop()
        if (!move) return

        move.undo(this.currentState)
        this.redoStack.push(move)
    }

    redoLastMove() {
        if (this.redoStack.isEmpty()) return

        const move = this.redoStack.pop()
        if (!move) return

        this.makeMove(move)
    }
}