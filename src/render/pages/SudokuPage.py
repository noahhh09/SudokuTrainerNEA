import sqlite3
from typing import Any

import customtkinter as ctk
import pandas as pd

from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.core.Move import Move, ValueChangeMove, CandidateChangeMove, EliminationChangeMove
from src.core.Game import Game
from src.render.components.SudokuGrid import SudokuGrid
from tests.test_board_state import createRandomBoardState

EDITING_STATES = {
    0: "Cell values",
    1: "Candidates",
    2: "Eliminated candidates"
}

class SudokuPage(ctk.CTkFrame):
    def __init__(self, master: Any, boardState: BoardState, mainMenuCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.place(relx=0.01, rely=0.05, anchor="w")

        self.boardState = boardState
        self.game = Game(self.boardState)

        self.sudokuGrid = SudokuGrid(self, self.game.boardState)
        self.sudokuGrid.place(relx=0.01, rely=0.1, anchor="nw")

        self.buttons = []
        self.buttonsContainer = ctk.CTkFrame(self)
        for i in range(1, 10):
            button = ctk.CTkButton(self.buttonsContainer, width=32, height=32,  text=str(i), command=lambda i=i: self.updateSelectedCellValue(i))
            button.grid(row=0, column=i - 1, padx=(0 if i == 1 else 2, 2))
            self.buttons.append(button)

        self.removeValueButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text=" ", command=lambda: self.updateSelectedCellValue(None))
        self.removeValueButton.grid(row=0, column=len(self.buttons), padx=(2,0))
        self.buttons.append(self.removeValueButton)

        self.undoButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text="Undo", command=self.__undo)
        self.undoButton.grid(row=0, column=len(self.buttons), padx=(10, 2))
        self.buttons.append(self.undoButton)

        self.redoButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text="Redo", command=self.__redo)
        self.redoButton.grid(row=0, column=len(self.buttons), padx=(2, 0))
        self.buttons.append(self.redoButton)

        self.editingState = 0
        self.editingStateButton = ctk.CTkButton(self.buttonsContainer, width=64, height=32, text="Editing: Cell values", command=self.incrementEditingState, fg_color="#2e8f01")
        self.editingStateButton.grid(row=0, column=len(self.buttons), padx=(10, 0))
        self.buttons.append(self.editingStateButton)

        self.buttonsContainer.place(relx=0.01, rely=0.99, anchor="sw")

        self.master.bind("<BackSpace>", lambda _: self.updateSelectedCellValue(None))
        self.master.bind("<KeyRelease>", lambda e: self.handleKeyPress(e))

    def incrementEditingState(self):
        self.editingState = (self.editingState + 1) % 3
        label = "Editing: " + EDITING_STATES[self.editingState]
        self.editingStateButton.configure(text=label)

    def updateSelectedCellValue(self, n: int | None):
        row, col = self.sudokuGrid.selectedCellPosition

        if row is None or col is None:
            return
        
        cell = self.game.boardState.getCell(row, col)
        move: Move | None = None
        match self.editingState:
            case 0: # Value editing
                oldValue = cell.getValue()

                if oldValue == n:
                    n = None

                move = ValueChangeMove(row, col, oldValue, n)

            case 1: # Candidate editing
                if n is not None:
                    wasAdded = n not in cell.getCandidates()
                    move = CandidateChangeMove(row, col, n, wasAdded)

            case 2: # Candidate elimination
                if n is not None:
                    wasAdded = n not in cell.getEliminatedCandidates()
                    move = EliminationChangeMove(row, col, n, wasAdded)
                
        if move is not None:
            self.game.makeMove(move)
            self.sudokuGrid.redrawCell(row, col) # Less heavy method than using grid.redraw()

    def handleKeyPress(self, event):
        shiftPressed = event.state & 0x1
        controlPressed = event.state & 0x4

        if event.char in "123456789" and len(event.char) == 1: 
            try:
                value = int(event.char)
                self.updateSelectedCellValue(value)
            except ValueError as e:
                pass

        elif controlPressed and event.keysym.lower() == "z":
            if shiftPressed:
                self.__redo()
            else:
                self.__undo()

    def __undo(self):
        self.game.undoLastMove()
        self.sudokuGrid.redraw() # Heavier method since the selected cell may not be the cell affected.

    def __redo(self):
        self.game.redoLastMove()
        self.sudokuGrid.redraw()