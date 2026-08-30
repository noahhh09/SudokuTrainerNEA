import json
import random
import sqlite3
from typing import Any

import tkinter as tk
import customtkinter as ctk
import pandas as pd

from src.core.BoardState import BoardState

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, master: Any, loadBoardStateCommand, techniquesPageCommand, accountsPageCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.loadBoardStateCommand = loadBoardStateCommand

        self.titleFont = ctk.CTkFont(size=48, weight="bold")
        self.buttonFont = ctk.CTkFont(size=24)

        self.titleLabel = ctk.CTkLabel(self, text="Learn Sudoku", font=self.titleFont)
        self.titleLabel.place(relx=0.5, rely=0.2, anchor="center")

        self.newPuzzleButton = ctk.CTkButton(self, text="New Puzzle", font=self.buttonFont, width=400, height=100, command=self.newPuzzle)
        self.newPuzzleButton.place(relx=0.5, rely=0.4, anchor="center")

        self.techniquesButton = ctk.CTkButton(self, text="Techniques Library", font=self.buttonFont, width=400, height=100, command=techniquesPageCommand)
        self.techniquesButton.place(relx=0.5, rely=0.6, anchor="center")

        self.accountButton = ctk.CTkButton(self, text="Account and Stats", font=self.buttonFont, width=400, height=100, command=accountsPageCommand)
        self.accountButton.place(relx=0.5, rely=0.8, anchor="center")

        # TODO - Remove, used to arbitrarily load a board state.
        entryInput = tk.StringVar()
        entryInput.set("x47f8fx3/x55fx28f/1fx23fx5/x37fx11f4fx2/4f2fx18fx27fx2/x42fx18fx2/x16f1f5f3f7fx24f/x41fx4/x48fx11fx19f")
        self.entry = ctk.CTkEntry(self, width=400, textvariable=entryInput)
        self.entry.place(anchor="nw")
        self.entry.bind("<Return>", lambda _: self.loadBoardStateCommand(BoardState.deserialise(self.entry.get())))

    def newPuzzle(self):
        conn = sqlite3.connect("sudoku.db")
        df = pd.read_sql_query("""
        SELECT P.PuzzleID, P.SerialisedBoard, P.clues, P.difficulty
        FROM Puzzles P
""", conn)

        if df.empty:
            print("No puzzles found")
            return

        randomIndex = random.randrange(len(df))
        puzzleData = json.loads(df.iloc[randomIndex].to_json())
        bs = BoardState.deserialise(puzzleData["SerialisedBoard"])
        self.loadBoardStateCommand(bs)
