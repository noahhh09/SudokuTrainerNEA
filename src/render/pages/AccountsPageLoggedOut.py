import sqlite3
from typing import Any

import bcrypt
import customtkinter as ctk

from src.render.components.ConfirmDeleteButton import ConfirmDeleteButton

class AccountsPageLoggedOut(ctk.CTkFrame):
    def __init__(self, master: Any, mainMenuCommand, setIdCommand, accountsPageCommand):
        super().__init__(master)
        self.setIdCommand = setIdCommand
        self.accountsPageCommand = accountsPageCommand

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

        mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        mainMenuButton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=10, columnspan=3)

        headerFont = ctk.CTkFont(size=24, weight="bold")

        # LOG IN 
        self.loginFrame = ctk.CTkScrollableFrame(self, border_width=2, height=400)
        self.loginFrame.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.loginFrame.grid_columnconfigure(0, weight=1)

        selectProfile_header = ctk.CTkLabel(self.loginFrame, text="Select Profile", font=headerFont)
        selectProfile_header.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.profileButtons: list[ctk.CTkBaseClass] = []
        self.buildProfileSelector()

        # CREATE PROFILE
        createProfileFrame = ctk.CTkFrame(self, border_width=2)
        createProfileFrame.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
        createProfileFrame.grid_columnconfigure(1, weight=1)

        createProfile_header = ctk.CTkLabel(createProfileFrame, text="Create Profile", font=headerFont)
        createProfile_header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        createProfile_nameEntryLabel = ctk.CTkLabel(createProfileFrame, text="Profile Name")
        createProfile_nameEntryLabel.grid(row=1, column=0, sticky="ew", padx=10)

        self.createProfile_nameEntry = ctk.CTkEntry(createProfileFrame, width=240)
        self.createProfile_nameEntry.grid(row=1, column=1, sticky="ew", padx=10)

        self.createProfile_statusLabel = ctk.CTkLabel(createProfileFrame, text="", wraplength=256)
        self.createProfile_statusLabel.grid(row=2, column=0, columnspan=2)

        createProfile_button = ctk.CTkButton(createProfileFrame, text="Create Profile", command=self.attemptSignup)
        createProfile_button.grid(row=5, column=0, columnspan=2, pady=10)

    def buildProfileSelector(self):
        for widget in self.profileButtons:
            widget.destroy()

        self.profileButtons = []
        conn = sqlite3.connect("sudoku.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT ProfileID, Name FROM Profiles
        """)

        profiles = cur.fetchall()
        for i, (id, name) in enumerate(profiles):
            profileButton = ctk.CTkButton(self.loginFrame, text=name, command=lambda id=id: self.selectProfile(id))
            profileButton.grid(row=i+1, column=0, pady=10, padx=(10,5), sticky="ew")

            deleteButton = ConfirmDeleteButton(self.loginFrame, text="Delete", fg_color="#aa0000", command=lambda id=id: self.deleteProfile(id))
            deleteButton.grid(row=i+1, column=1, pady=10, padx=(5,10), sticky="ew")

            self.profileButtons.append(profileButton)
            self.profileButtons.append(deleteButton)


    def selectProfile(self, id):
        self.setIdCommand(id)
        self.accountsPageCommand()

    def deleteProfile(self, id):
        conn = sqlite3.connect("sudoku.db")

        conn.execute("""
            DELETE FROM Profiles
            WHERE ProfileID = ?
        """, (id,))

        conn.commit()
        conn.close()

        self.buildProfileSelector()

    def attemptSignup(self):
        name = self.createProfile_nameEntry.get()

        if not (1 <= len(name) <= 32):
            self.createProfile_statusLabel.configure(text="Name must be between 1 and 32 characters long.")
            return

        conn = sqlite3.connect("sudoku.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Profiles ( 
                ProfileID INTEGER PRIMARY KEY AUTOINCREMENT, 
                Name TEXT NOT NULL UNIQUE,
                CreatedAt TIMESTAMP DEFAULT (unixepoch())
            );
        """) # Thank you https://stackoverflow.com/questions/11556546/sqlite-storing-default-timestamp-as-unixepoch

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Profiles (Name) VALUES (?)
            """, (name,))

            conn.commit()
            id = cursor.lastrowid
            self.setIdCommand(id)
            
        except sqlite3.IntegrityError:
            self.createProfile_statusLabel.configure(text="This account name is already taken.")

            cursor.execute("""
                SELECT ProfileID
                FROM Profiles
                WHERE Name = ?
            """, (name,))

            [id] = cursor.fetchone()
            self.setIdCommand(id)

        except sqlite3.Error:
            self.createProfile_statusLabel.configure(text="An unexpected error occurred.")

        self.accountsPageCommand()

        conn.close()
        

class AccountError(Exception):
    pass