from core.BoardState import BoardState


class Move:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def apply(self, board: BoardState):
        raise NotImplementedError

    def undo(self, board: BoardState):
        raise NotImplementedError


class ValueChangeMove(Move):
    def __init__(self, row: int, col: int, oldValue: int, newValue: int) -> None:
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

class CandidateChangeMove(Move):
    def __init__(self, row: int, col: int, candidateNumber: int, wasAdded: bool) -> None:
        super().__init__(row, col)
        self.candidateNumber = candidateNumber
        self.wasAdded = wasAdded

    # TODO Implement