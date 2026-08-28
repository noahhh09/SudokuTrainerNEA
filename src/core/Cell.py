class Cell:
    def __init__(self, value: int | None = None, editable: bool = False, candidates: set[int] | None = None, eliminatedCandidates: set[int] | None = None):
        self.__value = value
        self.__editable = editable

        if candidates is None:
            self.__candidates: set[int] = set()
        else:
            self.__candidates = candidates.copy()

        if eliminatedCandidates is None:
            self.__eliminatedCandidates = set()
        else:
            self.__eliminatedCandidates = eliminatedCandidates.copy()

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
            raise ValueError("Candidate value must be between 1 and 9 inclusive.")

        self.__candidates.add(value)

    def addCandidates(self, values: set[int]):
        for value in values:
            self.addCandidate(value)

    def removeCandidate(self, value: int):
        if not self.__editable:
            raise Exception("Cell is not editable.")

        if not value in self.__candidates:
            raise ValueError(f"Candidate {value} not present.")

        self.__candidates.remove(value)

    def getCandidates(self) -> set[int]:
        return self.__candidates.copy()

    def eliminateCandidate(self, value: int):
        if not self.__editable:
            raise Exception("Cell is not editable.")

        if not 1 <= value <= 9:
            raise ValueError("Eliminated candidate value must be between 1 and 9 inclusive")

        self.__eliminatedCandidates.add(value)

    def uneliminateCandidate(self, value: int):
        self.__eliminatedCandidates.remove(value)

    def getEliminatedCandidates(self) -> set[int]:
        return self.__eliminatedCandidates.copy()

    def getEffectiveCandidates(self) -> set[int]:
        if self.getValue() is not None:
            return set().copy()
            
        # Returns candidates ∩ (eliminated)'
        return set([candidate for candidate in self.__candidates if candidate not in self.__eliminatedCandidates])