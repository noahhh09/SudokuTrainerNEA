import sqlite3
from typing import Any

import customtkinter as ctk

class AccountsPageLoggedIn(ctk.CTkFrame):
    def __init__(self, master: Any, profileId: int, mainMenuCommand, setAccountIdCommand, accountsPageCommand):
        super().__init__(master)

        self.mainMenuCommand = mainMenuCommand
        self.setAccountIdCommand = setAccountIdCommand
        self.accountsPageCommand = accountsPageCommand

        conn = sqlite3.connect("sudoku.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Name
            FROM Profiles
            WHERE ProfileID = ?
        """, (profileId, ))

        name = cursor.fetchone()[0]
        headerFont = ctk.CTkFont(size=24, weight="bold")

        titleLabel = ctk.CTkLabel(self, text="Your Profile and Preferences", font=headerFont)
        titleLabel.place(relx=0.5, rely=0.1, anchor="center")

        nameLabel = ctk.CTkLabel(self, text=f"Welcome back, {name}")
        nameLabel.place(relx=0.5, rely=0.15, anchor="center")

        mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", command=mainMenuCommand)
        mainMenuButton.place(relx=0.4, rely=0.8, anchor="center")

        self.logoutButton = ctk.CTkButton(self, text="Log Out", command=self.logout)
        self.logoutButton.place(relx=0.6, rely=0.8, anchor="center")

    def logout(self):
        self.setAccountIdCommand(None)
        self.mainMenuCommand()