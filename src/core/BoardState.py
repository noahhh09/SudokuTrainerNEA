from .Cell import Cell

class BoardState:
    def __init__(self, cells):
        self.__cells: list[list[Cell]] = cells

    def getCell(self, row: int, col: int) -> Cell:
        return self.__cells[row][col]

    def getRow(self, rowIndex: int) -> list[Cell]:
        return self.__cells[rowIndex]

    def getColumn(self, colIndex: int) -> list[Cell]:
        return [self.__cells[i][colIndex] for i in range(9)]

    def getBlock(self, index: int) -> list[Cell]:
        startRow = (index // 3) * 3
        startCol = (index * 3) % 9

        result: list[Cell] = []

        for i in range(0, 3):
            for j in range(0, 3):
                result.append(self.__cells[startRow + i][startCol + j])

        return result

    def getBlockIndex(self, row: int, col: int) -> int:
        return (row // 3) * 3 + col // 3

    # Gets the position of the nth element inside a block.
    def getPositionInBlock(self, blockIndex: int, n: int) -> tuple[int, int]:
        row = (blockIndex // 3) * 3 + (n // 3)
        col = (blockIndex * 3) % 9 + (n % 3)

        return (row, col)

    """
    Returns the respective serialised string for the currently stored BoardState. 
    """
    def serialise(self) -> str:
        rowStrings: list[str]= []

        for row in self.__cells:
            successiveBlanks = 0
            thisRowStr = ""

            for j in range(9):
                value = row[j].getValue()

                if value is None:
                    successiveBlanks += 1
                else:
                    if successiveBlanks > 0:
                        thisRowStr += "x" + str(successiveBlanks)
                        successiveBlanks = 0

                    isEditable = row[j].isEditable()
                    thisRowStr += str(value) + ("t" if isEditable else "f")

            if successiveBlanks > 0:
                thisRowStr += "x" + str(successiveBlanks)

            rowStrings.append(thisRowStr)

        return "/".join(rowStrings)

    """
        Returns a BoardState formed from a serialised string.

        BoardState strings are split by a "/" for each row, then split into tokens of two characters each.
        xN = N empty, editable cells
        Nt = N in that cell, is editable
        Nf = N in that cell, is not editable
    """
    @staticmethod
    def deserialise(string: str) -> BoardState:
        finalArray = [[Cell(None, True) for _ in range(9)] for _ in range(9)]

        rowStrings = string.split("/")
        for i, row in enumerate(rowStrings):
            chunks: list[str] = [row[i:i+2] for i in range(0, len(row), 2)]

            currentCol = 0
            for token in chunks:
                if token[0] == "x": # Token represents token[1] successive empty, editable cells.
                    n = int(token[1])

                    for _ in range(n):
                        finalArray[i][currentCol] = Cell(None, True)
                        currentCol += 1

                else: # Token represents a value token[0] in cell. With token[1] indicating editability.
                    value = int(token[0])
                    isEditable = token[1] == "t"

                    finalArray[i][currentCol] = Cell(value, isEditable)
                    currentCol += 1

        return BoardState(finalArray)

    # Used for debugging. Makes BoardStates actually look nice when printed out.
    def __str__(self):
        string = "\n"

        for i in range(0, 9):
            for j in range(0, 9):
                string += str(self.__cells[i][j].getValue() or "x") + ","

            string = string.removesuffix(",")
            string += "\n"

        return string