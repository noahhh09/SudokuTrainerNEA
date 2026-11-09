import random
import sqlite3

import customtkinter as ctk

from src.analysis import ALL_TECHNIQUE_TYPES
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState

MAX_PER_ROW = 5

class TechniquesLibraryPage(ctk.CTkFrame):
    def __init__(self, master, mainMenuCommand, loadBoardStateCommand, techniquePageCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.place(relx=0.01, rely=0.05, anchor="w")

        self.statusLabel = ctk.CTkLabel(self, text="", fg_color='red', width=0)
        self.statusLabel.place(relx=0.5, rely=0.05, anchor="center")

        self.techniquesGrid = ctk.CTkScrollableFrame(self)

        for i, technique in enumerate(ALL_TECHNIQUE_TYPES):
            widget = TechniqueWidget(self.techniquesGrid, technique=technique, loadBoardStateCommand=loadBoardStateCommand, techniquePageCommand=techniquePageCommand, statusLabel=self.statusLabel)
            widget.grid(column=i % MAX_PER_ROW, row=i // MAX_PER_ROW, padx=(0 if i % MAX_PER_ROW == 0 else 5, 5), pady=(5, 5))

        self.techniquesGrid.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.8, anchor="n")


class TechniqueWidget(ctk.CTkFrame):
    def __init__(self, master, technique: type[Technique], loadBoardStateCommand, techniquePageCommand, statusLabel: ctk.CTkLabel, **kwargs): # I just want to say the type[Technique] thing is my coolest discovery yet.
        super().__init__(master, height=300, **kwargs)

        self.technique = technique
        self.statusLabel = statusLabel
        self.techniquePageCommand = techniquePageCommand
        self.loadBoardStateCommand = loadBoardStateCommand

        self.nameLabel = ctk.CTkLabel(self, text=technique.displayName, font=ctk.CTkFont(size=24, weight="bold"), wraplength=168)
        self.nameLabel.place(relx=0.5, rely=0.1, relwidth=1, anchor="n")

        self.descriptionLabel = ctk.CTkLabel(self, text=technique.description, wraplength=168, font=ctk.CTkFont(size=14))
        self.descriptionLabel.place(relx=0.5, rely=0.3, anchor="n")

        self.explainButton = ctk.CTkButton(self, text="Learn", command=self.explainTechnique)
        self.explainButton.place(relx=0.5, rely=0.8, anchor="center")

        self.practiceButton = ctk.CTkButton(self, text="Practice", command=self.practiceTechnique)
        self.practiceButton.place(relx=0.5, rely=0.9, anchor="center")

        count = 0 # Default value if the SELECT statement does not work.
        conn = sqlite3.connect("sudoku.db")
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT COUNT(*)
                FROM PuzzleTags Tag1
                INNER JOIN PuzzleTags Tag2
                    ON Tag1.PuzzleID = Tag2.PuzzleID
                WHERE Tag1.Tag = ?
                AND Tag2.Tag = 'solvable'
            """, (self.technique.__name__,))

            count = cur.fetchone()[0]
        except sqlite3.OperationalError as err:
            self.statusLabel.configure(text="Warning: puzzle tags could not be found. Have you set up the database using init_database.py?")
            print("Puzzle tags not found: ", err)
        
        conn.close()

        self.countLabel = ctk.CTkLabel(self, text=f"{count}", wraplength=168, font=ctk.CTkFont(size=10))
        self.countLabel.place(relx=0.5, rely=0.75, anchor="s")

    def explainTechnique(self):
        try:
            self.techniquePageCommand(self.technique)
        except NotImplementedError as err:
            self.statusLabel.configure(text="Sorry, this technique cannot be learned right now.")
            raise err

    def practiceTechnique(self):
        conn = sqlite3.connect("sudoku.db")
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT P.PuzzleID, P.SerialisedBoard, P.clues, P.difficulty
                FROM Puzzles P
                INNER JOIN PuzzleTags Tag1
                    ON P.PuzzleID = Tag1.PuzzleID
                INNER JOIN PuzzleTags Tag2
                    ON P.PuzzleID = Tag2.PuzzleID
                WHERE Tag1.Tag = ?
                AND Tag2.Tag = 'solvable'
            """, (self.technique.__name__,))
        except:
            pass

        results = cur.fetchall()
        conn.close()

        if len(results) == 0:
            self.statusLabel.configure(text="Sorry, no puzzles could be found. Have you set up the database using init_database.py?")
            return

        randomIndex = random.randrange(len(results))
        data = results[randomIndex]

        puzzleID = data[0]
        serialisedBoard = data[1]
        givens = data[2]
        difficulty = data[3]

        bs = BoardState.deserialise(serialisedBoard)
        self.loadBoardStateCommand(bs, puzzleID, givens, difficulty)