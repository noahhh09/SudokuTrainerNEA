import { Cell } from "./Cell"

export class BoardState {
    constructor(
        private cells: Cell[][]
    ) {}

    /**
     * Prints a BoardState in a more readable manner.
     */
    prettyPrint() {
        let string = "\n"

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                string += (this.cells[i][j].getCellValue() || "x") + ","
            }

            string = string.slice(0, string.length - 1)
            string += "\n"
        }

        console.log(string)
    }

    getCell(row: number, col: number): Cell {
        return this.cells[row][col]
    }

    getRow(index: number): Cell[] {
        return this.cells[index]
    }

    getColumn(index: number): Cell[] {
        return this.cells.map((_, colIndex) => this.cells.map(row => row[colIndex]))[index]
    }

    getBlock(index: number): Cell[] {
        const startRow = Math.floor(index / 3) * 3
        const startCol = (index * 3) % 9

        const result: Cell[] = []
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                result.push(this.cells[i + startRow][j + startCol])
            }
        }

        return result
    }

    getBlockIndex(row: number, col: number) {
        return Math.floor(row / 3) * 3 + Math.floor(col / 3)
    }

    /**
     * Returns an array of cells (in a similar way to BoardState) where each cell contains an array of all available candidates based on what values are in the current BoardState.
     */
    getAllCandidates(): number[][][] {
        /**
         * 1. Iterate through each empty cell:
         *  a. Add all 9 values to its potential candidates
         *  b. Check row -> remove all values in that row from candidates
         *  c. Do the same for the column, using transposition possibly
         *  d. Do the same for the box
         */
        const final: number[][][] = Array.from(
            { length: 9 },
            () => Array.from(
                { length: 9 },
                () => []
            )
        ); // GPT - Just creates an empty 9x9 array. Yes I'm lazy.

        const rowContents: number[][] = [[], [], [], [], [], [], [], [], []]
        const colContents: number[][] = [[], [], [], [], [], [], [], [], []]
        const blockContents: number[][] = [[], [], [], [], [], [], [], [], []]

        // Forms the row, column, and block arrays to more easily cross-check each row/col/block.
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const cell = this.cells[i][j]

                const value = cell.getCellValue()
                if (typeof value == "number") {
                    rowContents[i].push(value)
                    colContents[j].push(value)
                    blockContents[this.getBlockIndex(i, j)].push(value)
                }
            }
        }

        // Sets the available values in each row/col/block to all values NOT already in that row/col/block.
        const possibleCellValues = [1,2,3,4,5,6,7,8,9]
        const rowAvailables = rowContents.map(row => possibleCellValues.filter(value => !row.includes(value)))
        const colAvailables = colContents.map(col => possibleCellValues.filter(value => !col.includes(value)))
        const blockAvailables = blockContents.map(blk => possibleCellValues.filter(value => !blk.includes(value)))

        // Merges all row/col/block availables into one 9x9 "board-state-like" array representing all available digits in each cell in a given board state.
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.cells[i][j].getCellValue() == null) {
                    const block = this.getBlockIndex(i, j)

                    const intersection = rowAvailables[i].filter(
                        x => colAvailables[j].includes(x) && blockAvailables[block].includes(x)
                    );

                    final[i][j] = intersection
                }
            }
        }

        return final
    }

    /**
     * Returns a BoardState formed from a serialised string.
     * 
     * BoardState strings are split by a "/" for each row, then split into tokens of two characters each.
     * xN = N empty, editable cells
     * Nt = N in that cell, is editable
     * Nf = N in that cell, is not editable
     */
    static deserialise(str: string): BoardState {
        let finalBoardArray: Cell[][] = Array.from({ length: 9 }, () =>
            Array(9).fill(new Cell(null, true))
        );
        const rowStrings = str.split("/")

        let rowIdx = 0
        for (let row of rowStrings) {
            const chunks: string[] = [];
            
            for (let i = 0; i < row.length; i += 2) {
                chunks.push(row.slice(i, i + 2));
            }
            
            let currentSlot = 0
            for (let token of chunks) {
                if (token[0] == "x") {
                    for (let i = 0; i < parseInt(token[1]); i++) {
                        finalBoardArray[rowIdx][currentSlot] = new Cell(null, true)
                        currentSlot += 1
                    }
                }
                else {
                    const number = parseInt(token[0])
                    const isEditable = token[1] == "t"

                    finalBoardArray[rowIdx][currentSlot] = new Cell(number, isEditable)
                    currentSlot += 1
                }
            }
            rowIdx += 1
        }

        return new BoardState(finalBoardArray)
    }

    /**
     * Returns the respective serialised string for the currently stored BoardState. 
     */
    serialise(): string {
        let rows: string[] = []

        for (let row of this.cells) {
            let i = 0
            let successiveBlanks = 0

            let thisRowString = ""

            while (i < 9) {
                const cellValue = row[i].getCellValue()

                if (cellValue == null) {
                    successiveBlanks += 1
                } else {
                    const isEditable = row[i].isEditable()

                    if (successiveBlanks > 0) {
                        thisRowString += "x" + successiveBlanks.toString()
                        successiveBlanks = 0
                    }

                    thisRowString += cellValue.toString() + (isEditable ? "t" : "f")
                }

                i++
            }

            if (successiveBlanks > 0) {
                thisRowString += "x" + successiveBlanks.toString()
                successiveBlanks = 0
            }

            rows.push(thisRowString)
        }

        return rows.join("/")
    }
}