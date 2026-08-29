class Stack():
    def __init__(self) -> None:
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def clear(self):
        while not self.isEmpty():
            self.pop()

    def isEmpty(self) -> bool:
        return len(self.items) == 0