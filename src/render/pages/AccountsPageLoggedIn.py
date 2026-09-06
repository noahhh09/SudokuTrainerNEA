import sqlite3
from typing import Any

import customtkinter as ctk

class AccountsPageLoggedIn(ctk.CTkFrame):
    def __init__(self, master: Any, accountId: int, mainMenuCommand, accountsPageCommand):
        super().__init__(master)

        mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        mainMenuButton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=10)

        conn = sqlite3.connect("sudoku.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AccountName
            FROM Users
            WHERE UserID = ?
        """, (accountId, ))

        name = cursor.fetchone()[0]

        nameLabel = ctk.CTkLabel(self, text=f"Welcome back, {name}")
        nameLabel.grid(row=1,column=0, sticky="ew")