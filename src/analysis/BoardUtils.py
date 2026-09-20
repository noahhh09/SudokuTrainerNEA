from src.analysis.Unit import Unit, UnitType

from ..core.BoardState import BoardState


def _copyAndPopulateCandidates(board: BoardState) -> BoardState:
    board = BoardState.deserialise(board.serialise()) # Generates a copy of the same board without candidates and eliminations
    
    # 1. Iterate through each cell, and add its value, if applicable, to its respective row, col, and block's "contents"
    # 2. Filter down the list of all possible values (1 through 9) from each row/col/block, based on its contents. Essentially NOTing 1-9 with the contents above
    # 3. For each cell, find the INTERSECTION between the respective row, col, and block's available candidates for that cell.
    
    rowContents: list[set[int]] = [set() for _ in range(9)]
    colContents: list[set[int]] = [set() for _ in range(9)]
    blkContents: list[set[int]] = [set() for _ in range(9)]

    # Forms the row, column, and block arrays to more easily cross-check each row/col/block.
    for i in range(9):
        for j in range(9):
            value = board.getCell(i, j).getValue()

            if value is not None:
                rowContents[i].add(value)
                colContents[j].add(value)

                blkIndex = board.getBlockIndex(i, j)
                blkContents[blkIndex].add(value)

    possibleValues = {1,2,3,4,5,6,7,8,9}

    # Sets the available values in each row/col/block to all values NOT already in that row/col/block.
    rowAvailables = [possibleValues - row for row in rowContents]
    colAvailables = [possibleValues - col for col in colContents]
    blkAvailables = [possibleValues - blk for blk in blkContents]

    # Merges all row/col/block availables into one 9x9 "board-state-like" array representing all available digits in each cell in a given board state.
    # (essentially: rowAvailables ∩ colAvailables ∩ blkAvailables)
    for i in range(9):
        for j in range(9):
            if board.getCell(i, j).getValue() is not None:
                continue # We are only concerned about adding candidates to empty cells

            blockIdx = board.getBlockIndex(i, j)

            intersection = rowAvailables[i] & colAvailables[j] & blkAvailables[blockIdx]

            board.getCell(i, j).addCandidates(intersection)

    return board

"""
Creates a copy of the board and populates it with all logical candidates than can be deduced, retaining user-added eliminated candidates.
"""
def copyAndPopulateCandidates(board: BoardState) -> BoardState:
    newBoard = _copyAndPopulateCandidates(board)

    for i in range(9):
        for j in range(9):
            originallyEliminated = board.getCell(i, j).getEliminatedCandidates()
            newBoard.getCell(i, j).eliminateCandidates(originallyEliminated)

    return newBoard

def getMemberUnits(board: BoardState, row: int, col: int) -> list[Unit]:
    blockIndex = board.getBlockIndex(row, col)

    return [
        Unit(UnitType.Row, row, board.getRow(row)),
        Unit(UnitType.Column, col, board.getColumn(col)),
        Unit(UnitType.Block, blockIndex, board.getBlock(blockIndex)),
    ]

def getAllUnits(board: BoardState) -> list[Unit]:
    units: list[Unit] = []

    for i in range(9):
        units.append(Unit(UnitType.Row, i, board.getRow(i)))

    for j in range(9):
        units.append(Unit(UnitType.Column, j, board.getColumn(j)))

    for k in range(9):
        units.append(Unit(UnitType.Block, k, board.getBlock(k)))

    return units