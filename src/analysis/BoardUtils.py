from ..core.BoardState import BoardState

"""
    Returns an array of cells (in a similar way to BoardState) where each cell contains an array of all available candidates based on what values are in the current BoardState

    Filled cells will be treated as having no candidates regardless.
"""
def getAllCandidates(board: BoardState) -> list[list[list[int]]]:
    # 1. Iterate through each cell, and add its value, if applicable, to its respective row, col, and block's "contents"
    # 2. Filter down the list of all possible values (1 through 9) from each row/col/block, based on its contents. Essentially NOTing 1-9 with the contents above
    # 3. For each cell, find the INTERSECTION between the respective row, col, and block's available candidates for that cell.
    
    rowContents: list[list[int]] = [[] for _ in range(9)]
    colContents: list[list[int]] = [[] for _ in range(9)]
    blkContents: list[list[int]] = [[] for _ in range(9)]

    # Forms the row, column, and block arrays to more easily cross-check each row/col/block.
    for i in range(9):
        for j in range(9):
            value = board.getCell(i, j).getValue()

            if value != None:
                rowContents[i].append(value)
                colContents[j].append(value)

                blkIndex = board.getBlockIndex(i, j)
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
            if board.getCell(i, j).getValue() is not None:
                continue

            blockIdx = board.getBlockIndex(i, j)

            intersection = [
                value for value in rowAvailables[i] 
                if value in colAvailables[j] and value in blkAvailables[blockIdx]
            ]

            final[i][j] = intersection

    return final