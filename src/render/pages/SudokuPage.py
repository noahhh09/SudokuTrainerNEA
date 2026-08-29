from typing import Any

import customtkinter as ctk

from src.analysis import ALL_TECHNIQUES
from src.core.BoardState import BoardState
from src.core.Move import Move, ValueChangeMove, CandidateChangeMove, EliminationChangeMove
from src.core.Game import Game
from src.render.components.SudokuFeed import SudokuFeed
from src.render.components.SudokuControls import EditState, SudokuControls
from src.render.components.SudokuGrid import SudokuGrid

class SudokuPage(ctk.CTkFrame):
    def __init__(self, master: Any, boardState: BoardState, mainMenuCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=10)

        self.printBoardStateTodoRemove = ctk.CTkButton(self, text="Print Current State", width=200, height=50, command=lambda: print("Snapshot", self.game.boardState.serialise()))
        self.printBoardStateTodoRemove.grid(row=0, column=1, sticky="w", padx=(5, 0), pady=10)

        self.game = Game(boardState)

        self.sudokuGrid = SudokuGrid(self, self.game.boardState)
        self.sudokuGrid.grid(row=1, column=0, padx=5)

        self.controls = SudokuControls(self, root=self.master, updateSelectedCellCommand=self.updateSelectedCellValue, undoCommand=self.__undo, redoCommand=self.__redo)
        self.controls.grid(row=2, column=0, padx=5, pady=10)

        self.feed = SudokuFeed(self, self.game.boardState)
        self.feed.grid(row=1, column=1, sticky="nse")

    def __undo(self):
        self.game.undoLastMove()
        self.sudokuGrid.redraw() # Heavier method since the selected cell may not be the cell affected.
        self.feed.repopulate(self.game.boardState)

    def __redo(self):
        self.game.redoLastMove()
        self.sudokuGrid.redraw()
        self.feed.repopulate(self.game.boardState)

    def updateSelectedCellValue(self, n: int | None, editState: EditState):
        row, col = self.sudokuGrid.selectedCellPosition

        if row is None or col is None:
            return
        
        cell = self.game.boardState.getCell(row, col)
        move: Move | None = None

        match editState:
            case EditState.CELL_VALUES:
                if n == cell.getValue():
                    n = None

                move = ValueChangeMove(row, col, n)

            case EditState.CANDIDATES:
                if n is not None:
                    add = n not in cell.getCandidates()
                    move = CandidateChangeMove(row, col, n, add)

            case EditState.ELIMINATION:
                if n is not None:
                    add = n not in cell.getEliminatedCandidates()
                    move = EliminationChangeMove(row, col, n, add)
                
        if move is not None:
            self.game.makeMove(move)
            self.sudokuGrid.redraw()
            self.feed.repopulate(self.game.boardState)
