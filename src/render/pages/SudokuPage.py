from typing import Any

import customtkinter as ctk

from src.analysis import ALL_TECHNIQUES
from src.core.BoardState import BoardState
from src.core.Move import Move, ValueChangeMove, CandidateChangeMove, EliminationChangeMove
from src.core.Game import Game
from src.render.components.SudokuControls import EditState, SudokuControls
from src.render.components.SudokuGrid import SudokuGrid

class SudokuPage(ctk.CTkFrame):
    def __init__(self, master: Any, boardState: BoardState, mainMenuCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.place(relx=0.01, rely=0.05, anchor="w")

        self.game = Game(boardState)

        self.sudokuGrid = SudokuGrid(self, self.game.boardState)
        self.sudokuGrid.place(relx=0.01, rely=0.1, anchor="nw")

        self.controls = SudokuControls(self, self.master, self.updateSelectedCellValue, self.__undo, self.__redo)
        self.controls.place(relx=0.01, rely=0.99, anchor="sw")

    def __undo(self):
        self.game.undoLastMove()
        self.sudokuGrid.redraw() # Heavier method since the selected cell may not be the cell affected.

    def __redo(self):
        self.game.redoLastMove()
        self.sudokuGrid.redraw()

    def updateSelectedCellValue(self, n: int | None, editState: EditState):
        row, col = self.sudokuGrid.selectedCellPosition

        if row is None or col is None:
            return
        
        cell = self.game.boardState.getCell(row, col)
        move: Move | None = None

        match editState:
            case EditState.CELL_VALUES:
                oldValue = cell.getValue()

                if oldValue == n:
                    n = None

                move = ValueChangeMove(row, col, oldValue, n)

            case EditState.CANDIDATES:
                if n is not None:
                    wasAdded = n not in cell.getCandidates()
                    move = CandidateChangeMove(row, col, n, wasAdded)

            case EditState.ELIMINATION:
                if n is not None:
                    wasAdded = n not in cell.getEliminatedCandidates()
                    move = EliminationChangeMove(row, col, n, wasAdded)
                
        if move is not None:
            self.game.makeMove(move)
            self.sudokuGrid.redrawCell(row, col) # Less heavy method than using grid.redraw()