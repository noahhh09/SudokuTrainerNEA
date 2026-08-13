import { BoardState } from "./BoardState"

const s = "x9/".repeat(8) + "8f2tx63f"
const state = BoardState.deserialise(s)

state.getCell(2, 5).setCellValue(3)
state.getCell(5, 2).setCellValue(2)
state.getCell(1, 3).setCellValue(5)
state.getCell(1, 1).setCellValue(9)
state.getCell(0, 5).setCellValue(1)
state.getCell(8, 5).setCellValue(1)
state.getCell(2, 5).setCellValue(4)
let x = 0
while (x < 64) {
    x += 1
    const i = Math.floor(Math.random() * 9)
    const j = Math.floor(Math.random() * 9)
    const value = Math.floor(Math.random() * 9) + 1

    const cell = state.getCell(i, j)
    if (cell.isEditable()) {
        state.getCell(i, j).setCellValue(value)
    }
}

state.prettyPrint()

// console.log(state.getAllCandidates())

/**
 * What we need to be able to do in this section:
 * - Detect when a technique is available, probably by a pattern
 */

abstract class Technique {
    abstract checkIfAvailable(state: BoardState): boolean
}

class NakedSingle extends Technique {
    checkIfAvailable(state: BoardState): boolean {
        const candidates = state.getAllCandidates()
        let found = false

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (candidates[i][j].length == 1) {
                    console.log(`Found naked single at (${i}, ${j}) for value ${candidates[i][j][0]}`)
                    found = true
                }
            }
        }

        return found
    }
}

const foundNakedSingle = new NakedSingle().checkIfAvailable(state)
console.log(foundNakedSingle)