import json
import random
import sqlite3
from typing import Any

import tkinter as tk
import customtkinter as ctk
import pandas as pd

from src.core.BoardState import BoardState

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, master: Any, accountId: int | None, loadBoardStateCommand, techniquesPageCommand, accountsPageCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.loadBoardStateCommand = loadBoardStateCommand

        self.titleFont = ctk.CTkFont(size=48, weight="bold")
        self.buttonFont = ctk.CTkFont(size=24)

        self.titleLabel = ctk.CTkLabel(self, text="Learn Sudoku", font=self.titleFont)
        self.titleLabel.place(relx=0.5, rely=0.2, anchor="center")

        accountText = "You are not logged in. Progress will not be tracked."
        if accountId is not None:
            conn = sqlite3.connect("sudoku.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AccountName
                FROM Users
                WHERE UserID = ?
            """, (accountId, ))

            name = cursor.fetchone()[0]
            accountText = f"You are logged in as {name}."
        
        self.accountLabel = ctk.CTkLabel(self, text=accountText)
        self.accountLabel.place(relx=0.5, rely=0.3, anchor="s")

        self.newPuzzleButton = ctk.CTkButton(self, text="New Puzzle", font=self.buttonFont, width=400, height=100, command=self.newPuzzle)
        self.newPuzzleButton.place(relx=0.5, rely=0.4, anchor="center")

        self.techniquesButton = ctk.CTkButton(self, text="Techniques Library", font=self.buttonFont, width=400, height=100, command=techniquesPageCommand)
        self.techniquesButton.place(relx=0.5, rely=0.6, anchor="center")

        self.accountButton = ctk.CTkButton(self, text="Account and Stats", font=self.buttonFont, width=400, height=100, command=accountsPageCommand)
        self.accountButton.place(relx=0.5, rely=0.8, anchor="center")

        # TODO - Remove, used to arbitrarily load a board state.
        entryInput = tk.StringVar()
        entryInput.set("x14f1f7f2f9fx13fx1/7f6f9fx23f4fx12f/x13f2f6f4fx17f1f9f/4fx13f9fx21f7fx1/6fx17fx24f9fx13f/1f9f5f3f7fx22f4f/2f1f4f5f6f7f3f9f8f/3f7f6fx19fx15f4f1f/9f5f8f4f3f1f2f6f7f")
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
