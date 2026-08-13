export class Cell {
    constructor(
        private value: number | null = null,
        private editable: boolean
    ) {}

    setCellValue(input: number | null) {
        if (!this.editable) {
            throw Error("Cell is not editable")
        }

        if (!Number.isInteger(input)) {
            throw Error("Not an integer")
        }

        if (typeof input === "number" && (input > 9 || input < 0)) {
            throw Error("Not a number 1-9")
        }

        this.value = input
    }

    getCellValue(): number | null {
        return this.value
    }

    isEditable(): boolean {
        return this.editable
    }
}