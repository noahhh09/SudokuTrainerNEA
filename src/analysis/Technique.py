from ..core.Move import Move
from ..core.BoardState import BoardState

class Technique:
    displayName: str = ""
    description: str = ""

    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves

    @staticmethod
    def findAvailable(state: BoardState) -> list[Technique]:
        raise NotImplementedError()

    def identity(self) -> str:
        raise NotImplementedError()

    # Used for debugging.
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.moves})"

    # Used for debugging.
    def __repr__(self) -> str:
        return self.__str__()

