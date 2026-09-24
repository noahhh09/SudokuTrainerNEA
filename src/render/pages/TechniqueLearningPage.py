import random
import sqlite3

import customtkinter as ctk

from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.explanation.ExplanationFactory import ExplanationFactory
from src.explanation.TechniqueExplanation import TechniqueExplanation
from src.render.components.core.SudokuGrid import SudokuGrid

class TechniqueLearningPage(ctk.CTkFrame):
    def __init__(self, master, techniqueType: type[Technique], mainMenuCommand, customBoard: BoardState | None = None):
        super().__init__(master)
        techniqueId = techniqueType.__name__

        boardState = customBoard
        if customBoard is None: # Generate a random board state where the technique is available.
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

        elif type(boardState) is BoardState: # Verify the technique is available.
            if len(techniqueType.findAvailable(boardState)) == 0:
                raise ValueError("BoardState has no technique available.")

        if boardState is None: # Type hinting "hack"
            raise ValueError("Invalid or no BoardState provided.")

        self.grid_columnconfigure((1,2), weight=1)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=10)

        self.sudokuGrid = SudokuGrid(self, boardState) # Grid is not interactable without SudokuControls, so this is good for show.
        self.sudokuGrid.grid(row=1, column=0, padx=(5, 0), rowspan=2)

        titleFont = ctk.CTkFont(weight="bold", size=36)
        self.titleLabel = ctk.CTkLabel(self, text=techniqueType.displayName, font=titleFont)
        self.titleLabel.grid(row=0, column=1, columnspan=2)

        infoFont = ctk.CTkFont(size=18)
        self.infoLabel = ctk.CTkLabel(self, text="Info label", font=infoFont, wraplength=512)
        self.infoLabel.grid(row=1, column=1, columnspan=2, sticky="ew")

        self.technique = techniqueType.findAvailable(boardState)[0]
        self.explanation = ExplanationFactory.getExplanation(self.technique, boardState) # get the appropriate explanation for this technique type.
        self.explanation.getCurrent().apply(self.sudokuGrid, self.infoLabel) # load initial explanation step.

        self.advanceButton = ctk.CTkButton(self, command=self.previousStep, text="<")
        self.advanceButton.grid(row=2, column=1, sticky="ew")

        self.advanceButton = ctk.CTkButton(self, command=self.nextStep, text=">")
        self.advanceButton.grid(row=2, column=2, sticky="ew")


    def previousStep(self):
        current = self.explanation.getCurrent()
        current.undo(self.sudokuGrid, self.infoLabel)

        previous = self.explanation.getPrevious()
        previous.apply(self.sudokuGrid, self.infoLabel)

    def nextStep(self):
        current = self.explanation.getCurrent()
        current.undo(self.sudokuGrid, self.infoLabel)

        next = self.explanation.getNext()
        next.apply(self.sudokuGrid, self.infoLabel)
