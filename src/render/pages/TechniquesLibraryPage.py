import random
import sqlite3
import json

import customtkinter as ctk
import pandas as pd

from src.analysis import ALL_TECHNIQUE_TYPES
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState

MAX_PER_ROW = 5

class TechniquesLibraryPage(ctk.CTkFrame):
    def __init__(self, master, mainMenuCommand, loadBoardStateCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.place(relx=0.01, rely=0.05, anchor="w")

        self.techniquesGrid = ctk.CTkScrollableFrame(self)

        for i, technique in enumerate(ALL_TECHNIQUE_TYPES):
            widget = TechniqueWidget(self.techniquesGrid, technique=technique, loadBoardStateCommand=loadBoardStateCommand)
            widget.grid(column=i % MAX_PER_ROW, row=i // MAX_PER_ROW, padx=(0 if i % MAX_PER_ROW == 0 else 5, 5), pady=(5, 5))

        self.techniquesGrid.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.8, anchor="n")


class TechniqueWidget(ctk.CTkFrame):
    def __init__(self, master, technique: type[Technique], loadBoardStateCommand, **kwargs): # I just want to say the type[Technique] thing is my coolest discovery yet.
        super().__init__(master, height=300, **kwargs)

        self.technique = technique
        self.loadBoardStateCommand = loadBoardStateCommand

        self.nameLabel = ctk.CTkLabel(self, text=technique.displayName, font=ctk.CTkFont(size=24, weight="bold"), wraplength=168)
        self.nameLabel.place(relx=0.5, rely=0.1, relwidth=1, anchor="n")

        self.descriptionLabel = ctk.CTkLabel(self, text=technique.description, wraplength=168, font=ctk.CTkFont(size=14))
        self.descriptionLabel.place(relx=0.5, rely=0.3, anchor="n")

        self.explainButton = ctk.CTkButton(self, text="Learn")
        self.explainButton.place(relx=0.5, rely=0.8, anchor="center")

        self.practiceButton = ctk.CTkButton(self, text="Practice", command=self.practiceTechnique)
        self.practiceButton.place(relx=0.5, rely=0.9, anchor="center")

        conn = sqlite3.connect("sudoku.db")
        df = pd.read_sql_query("""
            SELECT COUNT(*) AS Count
            FROM PuzzleTags
            WHERE Tag = ?
        """, conn, params=(self.technique.__name__, ))
        conn.close()

        self.countLabel = ctk.CTkLabel(self, text=f"{df["Count"].iloc[0]}", wraplength=168, font=ctk.CTkFont(size=10,slant="italic"))
        self.countLabel.place(relx=0.5, rely=0.75, anchor="s")


    def practiceTechnique(self):
        conn = sqlite3.connect("sudoku.db")
        df = pd.read_sql_query("""
        SELECT P.PuzzleID, P.SerialisedBoard, P.clues, P.difficulty
        FROM Puzzles P
        INNER JOIN PuzzleTags
            ON P.PuzzleID = PuzzleTags.PuzzleID
        WHERE PuzzleTags.Tag = ?
""", conn, params=(self.technique.__name__,))
        conn.close()

        if df.empty:
            print("No puzzles found matching constraints")
            return

        randomIndex = random.randrange(len(df))
        puzzleData = json.loads(df.iloc[randomIndex].to_json())
        bs = BoardState.deserialise(puzzleData["SerialisedBoard"])
        self.loadBoardStateCommand(bs)
