from src.analysis import BoardUtils

from .BoardState import BoardState


class Move:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def apply(self, board: BoardState):
        raise NotImplementedError

    def undo(self, board: BoardState):
        raise NotImplementedError

    # Used for debugging.
    def __str__(self) -> str:
        return f"Move({self.row}, {self.col})"

    # Used for debugging.
    def __repr__(self) -> str:
        return self.__str__()


class ValueChangeMove(Move):
    def __init__(self, row: int, col: int, newValue: int | None) -> None:
        super().__init__(row, col)
        self.newValue = newValue

        self.oldValue: int | None = None
        self.applied = False
        self.removedCandidatePositions: list[tuple[int, int]] = []

    def apply(self, board: BoardState):
        cell = board.getCell(self.row, self.col)

        if cell.isEditable():
            if not self.applied:
                self.applied = True
                self.oldValue = cell.getValue()

            # O6.3. The system shall selectively remove candidates from cells in the same row/block/column if the user inputs a number into a cell.
            for unit in BoardUtils.getCellUnits(board, self.row, self.col):
                for i, subcell in enumerate(unit.cells):
                    if self.newValue in subcell.getCandidates():
                        subcell.removeCandidate(self.newValue)
                        self.removedCandidatePositions.append(unit.getBoardPosition(i))

            cell.setValue(self.newValue)

    def undo(self, board: BoardState):
        if not self.applied:
            raise ValueError("The move has not been applied yet.")

        cell = board.getCell(self.row, self.col)

        if cell.isEditable() and cell.getValue() == self.newValue:
            cell.setValue(self.oldValue)

            if self.newValue is not None:
                for row, col in self.removedCandidatePositions:
                    board.getCell(row, col).addCandidate(self.newValue)

    def __str__(self) -> str:
        return f"ValueChangeMove({self.row}, {self.col}, {self.oldValue}, {self.newValue})"

class CandidateChangeMove(Move):
    def __init__(self, row: int, col: int, candidateNumber: int, add: bool) -> None:
        super().__init__(row, col)
        self.candidateNumber = candidateNumber
        self.add = add

    def apply(self, board: BoardState):
        cell = board.getCell(self.row, self.col)

        if cell.isEditable() and cell.getValue() is None:
            if self.add:
                cell.addCandidate(self.candidateNumber)
            else:
                cell.removeCandidate(self.candidateNumber)

    def undo(self, board: BoardState):
        cell = board.getCell(self.row, self.col)
        
        if cell.isEditable() and cell.getValue() is None:
            if self.add:
                cell.removeCandidate(self.candidateNumber)
            else:
                cell.addCandidate(self.candidateNumber)

    def __str__(self) -> str:
        return f"CandidateChangeMove({self.row}, {self.col}, {self.candidateNumber}, {self.add})"

class EliminationChangeMove(Move):
    def __init__(self, row: int, col: int, candidateNumber: int, add: bool) -> None:
        super().__init__(row, col)
        self.candidateNumber = candidateNumber
        self.add = add

    def apply(self, board: BoardState):
        cell = board.getCell(self.row, self.col)

        if cell.isEditable() and cell.getValue() is None:
            if self.add:
                cell.eliminateCandidate(self.candidateNumber)
            else:
                cell.uneliminateCandidate(self.candidateNumber)

    def undo(self, board: BoardState):
        cell = board.getCell(self.row, self.col)
        
        if cell.isEditable() and cell.getValue() is None:
            if self.add:
                cell.uneliminateCandidate(self.candidateNumber)
            else:
                cell.eliminateCandidate(self.candidateNumber)

    def __str__(self) -> str:
        return f"EliminationChangeMove({self.row}, {self.col}, {self.candidateNumber}, {self.add})"