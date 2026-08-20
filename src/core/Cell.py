class Cell:
    def __init__(self, value: int | None = None, editable: bool = False, candidates: set[int] = set()):
        self.__value = value
        self.__editable = editable
        self.__candidates = candidates

    def setValue(self, value: int | None):
        if not self.__editable:
            raise Exception("Cell is not editable.")

        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Input is not an int or None")

            if value < 1 or value > 9:
                raise ValueError("Value must be between 1 and 9 inclusive, or None.")
        
        self.__value = value
    
    def getValue(self) -> int | None:
        return self.__value

    def isEditable(self) -> bool:
        return self.__editable

    def addCandidate(self, value: int):
        if not self.__editable:
            raise Exception("Cell is not editable.")

        if not 1 <= value <= 9:
            raise ValueError("Value must be between 1 and 9 inclusive.")

        self.__candidates.add(value)

    def removeCandidate(self, value: int):
        if not self.__editable:
            raise Exception("Cell is not editable.")

        if not value in self.__candidates:
            raise ValueError(f"Candidate {value} not present.")

        self.__candidates.remove(value)

    def getCandidates(self) -> set[int]:
        return self.__candidates