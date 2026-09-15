import random
import sqlite3

import customtkinter as ctk

from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.render.components.core.SudokuGrid import SudokuGrid

class TechniqueLearningPage(ctk.CTkFrame):
    def __init__(self, master, technique: type[Technique], mainMenuCommand, **kwargs):
        super().__init__(master, **kwargs)
        self.technique = technique

        techniqueId = technique.__name__

        conn = sqlite3.connect("sudoku.db")

        cur = conn.cursor()
        cur.execute("""
            SELECT Puzzles.SerialisedBoard
            FROM Puzzles
            INNER JOIN PuzzleTags
                ON Puzzles.PuzzleID = PuzzleTags.PuzzleID
            WHERE PuzzleTags.Tag = ?
        """, (techniqueId,))

        found = cur.fetchall()
        randomIndex = random.randint(0, len(found) - 1)
        boardString = found[randomIndex][0]
        boardState = BoardState.deserialise(boardString)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=10)

        self.sudokuGrid = SudokuGrid(self, boardState) # Grid is not interactable without SudokuControls, so this is good for show.
        self.sudokuGrid.grid(row=1, column=0, padx=(5, 0), rowspan=2)

        titleFont = ctk.CTkFont(weight="bold", size=36)
        self.titleLabel = ctk.CTkLabel(self, text=technique.displayName, font=titleFont)
        self.titleLabel.grid(row=0, column=1)

        