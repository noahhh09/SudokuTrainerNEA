from ..core.Move import Move
from ..core.BoardState import BoardState

class Technique:
    displayName: str = ""
    description: str = ""

    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves

    @classmethod # Similar to static methods, but allows class variables to be accessed (useful for multi-degree classes, like NakedGroup). https://www.geeksforgeeks.org/python/classmethod-in-python/
    def findAvailable(cls, state: BoardState) -> list[Technique]:
        raise NotImplementedError()

    def identity(self) -> str:
        raise NotImplementedError()

    def getHintData(self) -> dict[str, str]:
        raise NotImplementedError()

    # Used for debugging.
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.moves})"

    # Used for debugging.
    def __repr__(self) -> str:
        return self.__str__()
