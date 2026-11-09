import getopt
import random
import sqlite3
import sys
from typing import Any

import tkinter as tk
import customtkinter as ctk

from src.core.BoardState import BoardState
from src.render.components.CTkRangeSlider import CTkRangeSlider

DEV_MODE = False

# Command line developer mode
# https://www.geeksforgeeks.org/python/command-line-arguments-in-python/
try:
    args, values = getopt.getopt(sys.argv[1:], "d", ["dev"])
    for arg, value in args:
        if arg in ("-d", "-dev"):
            DEV_MODE = True
except:
    pass # Ignores errors if no flags are specified, or other unrelated flags are.

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, master: Any, profileId: int | None, loadBoardStateCommand, techniquesPageCommand, accountsPageCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.loadBoardStateCommand = loadBoardStateCommand

        self.titleFont = ctk.CTkFont(size=48, weight="bold")
        self.buttonFont = ctk.CTkFont(size=24)

        self.titleLabel = ctk.CTkLabel(self, text="Learn Sudoku", font=self.titleFont)
        self.titleLabel.place(relx=0.5, rely=0.2, anchor="center")

        accountText = "You have not selected a profile. Progress will not be tracked."
        if profileId is not None:
            conn = sqlite3.connect("sudoku.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Name
                FROM Profiles
                WHERE ProfileID = ?
            """, (profileId, ))

            accountName = cursor.fetchone()[0]
            accountText = f"You are using the {accountName} profile."

        ### BUTTONS
        
        self.accountLabel = ctk.CTkLabel(self, text=accountText)
        self.accountLabel.place(relx=0.5, rely=0.3, anchor="s")

        self.newPuzzleButton = ctk.CTkButton(self, text="New Puzzle", font=self.buttonFont, width=400, height=100, command=self.newPuzzle)
        self.newPuzzleButton.place(relx=0.5, rely=0.4, anchor="center")

        ### DIFFICULTY SELECT
        # O3.1 The user shall be able to determine a range of difficulty levels (if they choose).

        minDiff, maxDiff = self.getAvailableDifficultyRange()

        self.difficultySelectFrame = ctk.CTkFrame(self)
        self.difficultySelectFrame.place(relx=0.5, rely=0.5, anchor="center")

        self.diffLabel = ctk.CTkLabel(self.difficultySelectFrame, text="Difficulty", font=ctk.CTkFont(weight='bold'))
        self.diffLabel.grid(row=0, column=0, padx=(5, 0))

        self.minDiffLabel = ctk.CTkLabel(self.difficultySelectFrame, text=minDiff)
        self.minDiffLabel.grid(row=0, column=1, padx=(5, 0))

        self.difficultySlider = CTkRangeSlider(self.difficultySelectFrame, from_=minDiff * 10, to=maxDiff * 10, command=self.updateDifficultySliderLabels)
        self.difficultySlider.grid(row=0, column=2, padx=5)

        self.maxDiffLabel = ctk.CTkLabel(self.difficultySelectFrame, text=maxDiff)
        self.maxDiffLabel.grid(row=0, column=3, padx=(0, 5))

        ### EVERYTHING ELSE

        self.techniquesButton = ctk.CTkButton(self, text="Techniques Library", font=self.buttonFont, width=400, height=100, command=techniquesPageCommand)
        self.techniquesButton.place(relx=0.5, rely=0.65, anchor="center")

        self.accountButton = ctk.CTkButton(self, text="Account and Stats", font=self.buttonFont, width=400, height=100, command=accountsPageCommand)
        self.accountButton.place(relx=0.5, rely=0.85, anchor="center")

        if DEV_MODE:
            boardInputVar = tk.StringVar()
            boardInputVar.set("x14f1f7f2f9fx13fx1/7f6f9fx23f4fx12f/x13f2f6f4fx17f1f9f/4fx13f9fx21f7fx1/6fx17fx24f9fx13f/1f9f5f3f7fx22f4f/2f1f4f5f6f7f3f9f8f/3f7f6fx19fx15f4f1f/9f5f8f4f3f1f2f6f7f")
            self.boardEntry = ctk.CTkEntry(self, width=400, textvariable=boardInputVar)
            self.boardEntry.place(anchor="nw")
            self.boardEntry.bind("<Return>", lambda _: self.loadBoardStateCommand(BoardState.deserialise(self.boardEntry.get())))

    def newPuzzle(self):
        minDiff, maxDiff = self.getSelectedDifficultyRange()
        
        conn = sqlite3.connect("sudoku.db")
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT Puzzles.PuzzleID, SerialisedBoard, clues, difficulty
                FROM Puzzles
                INNER JOIN PuzzleTags
                    ON Puzzles.PuzzleID = PuzzleTags.PuzzleID
                WHERE TAG ='solvable'
                AND difficulty >= ?
                AND difficulty <= ?
            """, (minDiff, maxDiff))
        except sqlite3.OperationalError as err:
            print("Puzzles table not created.")
            self.accountLabel.configure(text="No puzzles found! Have you set up the puzzle database yet? See README.md for more info.")
            self.accountLabel.configure(fg_color='red')
            raise err

        results = cur.fetchall()
        conn.close()

        if len(results) == 0:
            self.accountLabel.configure(text="No puzzles found matching these constraints!")
            self.accountLabel.configure(fg_color='red')
            return

        randomIndex = random.randrange(len(results))
        data = results[randomIndex]

        puzzleID = data[0]
        serialisedBoard = data[1]
        givens = data[2]
        difficulty = data[3]

        bs = BoardState.deserialise(serialisedBoard)
        self.loadBoardStateCommand(bs, puzzleID, givens, difficulty)

    def getAvailableDifficultyRange(self):
        conn = sqlite3.connect("sudoku.db")
        cur = conn.cursor()

        # Thank you https://stackoverflow.com/questions/45061067/select-the-row-with-maximum-minimum-value-in-sqlite for help with syntax.
        # TODO - Defensive programming
        cur.execute("""
            SELECT MIN(difficulty), MAX(difficulty)
            FROM Puzzles
            INNER JOIN PuzzleTags
                ON Puzzles.PuzzleID = PuzzleTags.PuzzleID
            WHERE PuzzleTags.Tag = 'solvable'
        """)

        return cur.fetchone()

    def getSelectedDifficultyRange(self):
        minDiff, maxDiff = self.difficultySlider.get()
        return (minDiff // 1) / 10, (maxDiff // 1) / 10

    def updateDifficultySliderLabels(self, argument):
        minDiff, maxDiff = self.getSelectedDifficultyRange()

        self.minDiffLabel.configure(text=str(minDiff))
        self.maxDiffLabel.configure(text=str(maxDiff))