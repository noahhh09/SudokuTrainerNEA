from .Cell import Cell

class BoardState:
    def __init__(self, cells):
        self.__cells: list[list[Cell]] = cells

    def getCell(self, row: int, col: int) -> Cell:
        return self.__cells[row][col]

    def getRow(self, rowIndex: int) -> list[Cell]:
        return self.__cells[rowIndex]

    # getColumn() NOT IMPLEMENTED!
    # Original TS Code:
    #
    # getColumn(index: number): Cell[] {
    #     return this.cells.map((_, colIndex) => this.cells.map(row => row[colIndex]))[index]
    # }
    #

    def getColumn(self, colIndex: int) -> list[Cell]:
        raise NotImplementedError()

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

    """
        Returns an array of cells (in a similar way to BoardState) where each cell contains an array of all available candidates based on what values are in the current BoardState
    """
    def getAllCandidates(self) -> list[list[list[int]]]:
        # 1. Iterate through each cell, and add its value, if applicable, to its respective row, col, and block's "contents"
        # 2. Filter down the list of all possible values (1 through 9) from each row/col/block, based on its contents. Essentially NOTing 1-9 with the contents above
        # 3. For each cell, find the INTERSECTION between the respective row, col, and block's available candidates for that cell.
        
        rowContents: list[list[int]] = [[] for _ in range(9)]
        colContents: list[list[int]] = [[] for _ in range(9)]
        blkContents: list[list[int]] = [[] for _ in range(9)]

        # Forms the row, column, and block arrays to more easily cross-check each row/col/block.
        for i in range(9):
            for j in range(9):
                cell = self.__cells[i][j]
                value = cell.getValue()

                if value != None:
                    rowContents[i].append(value)
                    colContents[j].append(value)

                    blkIndex = self.getBlockIndex(i, j)
                    blkContents[blkIndex].append(value)

        possibleValues = [1,2,3,4,5,6,7,8,9]

        # Sets the available values in each row/col/block to all values NOT already in that row/col/block.
        rowAvailables = [[value for value in possibleValues if value not in row] for row in rowContents]
        colAvailables = [[value for value in possibleValues if value not in col] for col in colContents]
        blkAvailables = [[value for value in possibleValues if value not in blk] for blk in blkContents]

        # (9x9x9) A list of all cells, each with a list of possible candidates in that cell.
        final: list[list[list[int]]] = [[[] for _ in range(9)] for _ in range(9)]

        # Merges all row/col/block availables into one 9x9 "board-state-like" array representing all available digits in each cell in a given board state.
        # (essentially: rowAvailables ∩ colAvailables ∩ blkAvailables)
        for i in range(9):
            for j in range(9):
                if self.__cells[i][j].getValue() is None:
                    continue

                blockIdx = self.getBlockIndex(i, j)

                intersection = [
                    value for value in rowAvailables[i] 
                    if value in colAvailables[j] and value in blkAvailables[blockIdx]
                ]

                final[i][j] = intersection

        return final

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
        
    def __str__(self):
        string = "\n"

        for i in range(0, 9):
            for j in range(0, 9):
                string += str(self.__cells[i][j].getValue() or "x") + ","

            string = string.removesuffix(",")
            string += "\n"

        return string