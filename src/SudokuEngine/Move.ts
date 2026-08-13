import { BoardState } from "./BoardState";

export interface Move {
    row: number,
    col: number,

    apply(board: BoardState): void
    undo(board: BoardState): void
}

export class ValueChangeMove implements Move {
    constructor(
        public row: number,
        public col: number,
        public oldValue: number,
        public newValue: number
    ) {}

    apply(board: BoardState) {
        const cell = board.getCell(this.row, this.col)

        // TODO - Might be worth checking if the value of the cell == oldValue?
        if (cell.isEditable()) {
            cell.setCellValue(this.newValue)
        }
    }

    undo(board: BoardState) {
        const cell = board.getCell(this.row, this.col)

        // TODO - Might be worth checking if the value of the cell == newValue?
        if (cell.isEditable()) {
            cell.setCellValue(this.oldValue)
        }
    }
}

export class CandidateChangeMove implements Move {
    constructor(
        public row: number,
        public col: number,
        public number: number,
        public added: boolean
    ) {
        console.log("Warning - CandidateChangeMove is not fully implemented!")
    }

    apply(board: BoardState) {
        const cell = board.getCell(this.row, this.col)

        if (cell.isEditable()) {
            // TODO
            console.log("Warning - apply() not implemented for CandidateChangeMove")
        }
    }

    undo(board: BoardState) {
        const cell = board.getCell(this.row, this.col)
        
        if (cell.isEditable()) {
            // TODO
            console.log("Warning - undo() not implemented for CandidateChangeMove")
        }
    }
}