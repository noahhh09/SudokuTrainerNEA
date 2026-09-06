from typing import Any, Tuple
from enum import Enum

import customtkinter as ctk


class EditState(Enum):
    CELL_VALUES = (0, "Cell values")
    CANDIDATES = (1, "Candidates")
    ELIMINATION = (2, "Eliminated candidates")

    def __init__(self, id: int, displayName: str) -> None:
        self.id = id
        self.displayName = displayName

    def next(self) -> EditState:
        id = self.id + 1 % len(EditState)
        return EditState.fromId(id)

    # AI disclosure - Asked "How do i get a state from an id?" along with this enum's definition, entries and its __init__ function only.
    @staticmethod
    def fromId(id: int) -> EditState:
        for state in EditState:
            if state.id == id:
                return state

        return EditState.CELL_VALUES

class SudokuControls(ctk.CTkFrame):
    def __init__(self, master: Any, root: Any, updateSelectedCellCommand, undoCommand, redoCommand, **kwargs):
        super().__init__(master, **kwargs)
        self.editingState: EditState = EditState.CELL_VALUES

        self.updateSelectedCellCommand = updateSelectedCellCommand
        self.undoCommand = undoCommand
        self.redoCommand = redoCommand

        root.bind("<BackSpace>", lambda _: self.updateSelectedCellCommand(None, self.editingState))
        root.bind("<KeyRelease>", lambda e: self.handleKeyPress(e))
        
        self.buttons = []
        self.buttonsContainer = ctk.CTkFrame(self)

        for i in range(1, 10):
            button = ctk.CTkButton(self.buttonsContainer, width=32, height=32,  text=str(i), command=lambda i=i: self.updateSelectedCellCommand(i, self.editingState))
            button.grid(row=0, column=i - 1, padx=(0 if i == 1 else 2, 2))
            self.buttons.append(button)

        self.removeValueButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text=" ", command=lambda: self.updateSelectedCellCommand(None, self.editingState))
        self.removeValueButton.grid(row=0, column=len(self.buttons), padx=(2,0))
        self.buttons.append(self.removeValueButton)

        self.undoButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text="Undo", command=undoCommand)
        self.undoButton.grid(row=0, column=len(self.buttons), padx=(10, 2))
        self.buttons.append(self.undoButton)

        self.redoButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text="Redo", command=redoCommand)
        self.redoButton.grid(row=0, column=len(self.buttons), padx=(2, 0))
        self.buttons.append(self.redoButton)

        self.editingStateButton = ctk.CTkButton(self.buttonsContainer, width=64, height=32, text="Editing: Cell values", command=self.incrementEditingState, fg_color="#2e8f01")
        self.editingStateButton.grid(row=0, column=len(self.buttons), padx=(10, 0))
        self.buttons.append(self.editingStateButton)

        self.buttonsContainer.pack(fill="both", expand=True)

    def incrementEditingState(self):
        self.editingState = self.editingState.next()
        label = "Editing: " + self.editingState.displayName
        self.editingStateButton.configure(text=label)

    def getEditingState(self):
        return self.editingState

    def handleKeyPress(self, event):
        shiftPressed = event.state & 0x1
        controlPressed = event.state & 0x4

        if event.char in "123456789" and len(event.char) == 1: 
            try:
                value = int(event.char)
                self.updateSelectedCellCommand(value, self.editingState)
            except ValueError as e:
                pass

        elif controlPressed and event.keysym.lower() == "z":
            if shiftPressed:
                self.redoCommand
            else:
                self.undoCommand

