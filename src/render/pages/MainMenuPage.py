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
        entryInput.set("5fx37f8f9fx2/6fx12f1fx34f8f/1f9fx13fx25fx17f/x15fx17f6f1f4f2f3f/x26f8f5f3fx19f1f/x11f3fx12fx36f/9f6f1fx27f2f8f4f/2fx56f3f5f/x14f5fx31f7f9f")
        self.entry = ctk.CTkEntry(self, width=400, textvariable=entryInput)
        self.entry.place(anchor="nw")
        self.entry.bind("<Return>", lambda _: self.loadBoardStateCommand(BoardState.deserialise(self.entry.get())))

    def newPuzzle(self):
        conn = sqlite3.connect("sudoku.db")
        df = pd.read_sql_query("""
        SELECT P.PuzzleID, P.SerialisedBoard, P.clues, P.difficulty
        FROM Puzzles P
        ORDER BY RANDOM()
        LIMIT 1
""", conn)

        if df.empty:
            print("No puzzles found")
            return

        bs = BoardState.deserialise(df.iloc[0]["SerialisedBoard"])
        self.loadBoardStateCommand(bs)
        print(df.iloc[0].to_json())
