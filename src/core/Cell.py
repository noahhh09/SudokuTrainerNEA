class Cell:
    def __init__(self, value: int | None = None, editable: bool = False):
        self.__value = value
        self.__editable = editable

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