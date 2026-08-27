from typing import Any

import customtkinter as ctk

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, master: Any, newPuzzleCommand, techniquesPageCommand, accountsPageCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.titleFont = ctk.CTkFont(size=48, weight="bold")
        self.buttonFont = ctk.CTkFont(size=24)

        self.titleLabel = ctk.CTkLabel(self, text="Learn Sudoku", font=self.titleFont)
        self.titleLabel.place(relx=0.5, rely=0.2, anchor="center")

        self.newPuzzleButton = ctk.CTkButton(self, text="New Puzzle", font=self.buttonFont, width=400, height=100, command=newPuzzleCommand)
        self.newPuzzleButton.place(relx=0.5, rely=0.4, anchor="center")

        self.techniquesButton = ctk.CTkButton(self, text="Techniques Library", font=self.buttonFont, width=400, height=100, command=techniquesPageCommand)
        self.techniquesButton.place(relx=0.5, rely=0.6, anchor="center")

        self.accountButton = ctk.CTkButton(self, text="Account and Stats", font=self.buttonFont, width=400, height=100, command=accountsPageCommand)
        self.accountButton.place(relx=0.5, rely=0.8, anchor="center")
