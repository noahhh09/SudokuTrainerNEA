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
    def __init__(self, row: int, col: int, oldValue: int | None, newValue: int | None) -> None:
        super().__init__(row, col)
        self.oldValue = oldValue
        self.newValue = newValue

    def apply(self, board: BoardState):
        cell = board.getCell(self.row, self.col)

        # TODO - Might be worth checking if the value of the cell == oldValue?
        if cell.isEditable():
            cell.setValue(self.newValue)

    def undo(self, board: BoardState):
        cell = board.getCell(self.row, self.col)

        # TODO - Might be worth checking if the value of the cell == newValue?
        if cell.isEditable():
            cell.setValue(self.oldValue)

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