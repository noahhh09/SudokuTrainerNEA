import sqlite3
from typing import Any

import bcrypt
import customtkinter as ctk

class AccountsPageLoggedOut(ctk.CTkFrame):
    def __init__(self, master: Any, mainMenuCommand, setIdCommand, accountsPageCommand):
        super().__init__(master)
        self.setIdCommand = setIdCommand
        self.accountsPageCommand = accountsPageCommand

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        mainMenuButton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=10)

        headerFont = ctk.CTkFont(size=24, weight="bold")

        # LOG IN 
        loginFrame = ctk.CTkFrame(self, border_width=2)
        loginFrame.grid(row=1, column=0, sticky="e", padx=10, pady=50)

        loginFrame.grid_columnconfigure((0, 1), weight=1)

        login_header = ctk.CTkLabel(loginFrame, text="Log In", font=headerFont)
        login_header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        login_accountEntryLabel = ctk.CTkLabel(loginFrame, text="Account Name")
        login_accountEntryLabel.grid(row=1, column=0, sticky="w", padx=10)

        self.login_accountEntry = ctk.CTkEntry(loginFrame, width=240)
        self.login_accountEntry.grid(row=1, column=1, sticky="e", padx=10)

        login_passwordEntryLabel = ctk.CTkLabel(loginFrame, text="Password")
        login_passwordEntryLabel.grid(row=2, column=0, sticky="w", padx=10)

        self.login_passwordEntry = ctk.CTkEntry(loginFrame, width=240, show="*")
        self.login_passwordEntry.grid(row=2, column=1, sticky="e", padx=10)

        self.login_statusLabel = ctk.CTkLabel(loginFrame, text="", wraplength=196)
        self.login_statusLabel.grid(row=3, column=0, columnspan=2)

        login_button = ctk.CTkButton(loginFrame, text="Log In", command=self.attemptLogin)
        login_button.grid(row=4, column=0, columnspan=2)

        # SIGN UP
        signupFrame = ctk.CTkFrame(self, border_width=2)
        signupFrame.grid(row=1, column=1, sticky="w", padx=10, pady=50)

        signup_header = ctk.CTkLabel(signupFrame, text="Sign Up", font=headerFont)
        signup_header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        signup_accountEntryLabel = ctk.CTkLabel(signupFrame, text="Account Name")
        signup_accountEntryLabel.grid(row=1, column=0, sticky="w", padx=10)

        self.signup_accountEntry = ctk.CTkEntry(signupFrame, width=240)
        self.signup_accountEntry.grid(row=1, column=1, sticky="e", padx=10)

        signup_passwordEntryLabel = ctk.CTkLabel(signupFrame, text="Password")
        signup_passwordEntryLabel.grid(row=2, column=0, sticky="w", padx=10)

        self.signup_passwordEntry = ctk.CTkEntry(signupFrame, width=240, show="*")
        self.signup_passwordEntry.grid(row=2, column=1, sticky="e", padx=10)

        signup_passwordVerifyLabel = ctk.CTkLabel(signupFrame, text="Verify Password")
        signup_passwordVerifyLabel.grid(row=3, column=0, sticky="w", padx=10)

        self.signup_passwordVerifyEntry = ctk.CTkEntry(signupFrame, width=240, show="*")
        self.signup_passwordVerifyEntry.grid(row=3, column=1, sticky="e", padx=10)

        self.signup_statusLabel = ctk.CTkLabel(signupFrame, text="", wraplength=196)
        self.signup_statusLabel.grid(row=4, column=0, columnspan=2)

        signup_button = ctk.CTkButton(signupFrame, text="Sign Up", command=self.attemptSignup)
        signup_button.grid(row=5, column=0, columnspan=2)

    def attemptLogin(self):
        account = self.login_accountEntry.get()
        enteredPassword = self.login_passwordEntry.get()

        if not (3 <= len(account) <= 32) or not (8 <= len(enteredPassword) <= 128):
            self.login_statusLabel.configure(text="Account name must be between 3 and 32 characters long. Password must be between 8 and 128.")
            return

        conn = sqlite3.connect("sudoku.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT UserID, Salt, HashedPassword
            FROM Users
            WHERE AccountName = ?
        """, (account,))

        data = cur.fetchone()
        if data is None:
            self.login_statusLabel.configure(text="Incorrect username/password.") # Good for privacy to not reveal WHAT was specifically wrong. (since it reveals an account exists otherwise)
            return

        id, salt, hashedPassword = data

        enteredBytes = enteredPassword.encode('utf-8')
        enteredHashed = bcrypt.hashpw(enteredBytes, salt)

        if enteredHashed != hashedPassword:
            self.login_statusLabel.configure(text="Incorrect username/password.") # Good for privacy to not reveal WHAT was specifically wrong. (since it reveals an account exists otherwise)
            return

        self.setIdCommand(id)
        self.accountsPageCommand()

        conn.close()


    def attemptSignup(self):
        name = self.signup_accountEntry.get()
        password = self.signup_passwordEntry.get()
        verify = self.signup_passwordVerifyEntry.get()

        if  not (3 <= len(name) <= 32) or not (8 <= len(password) <= 128) or not (8 <= len(verify) <= 128):
            self.signup_statusLabel.configure(text="Name must be between 3 and 32 characters long. Password must be between 8 and 128.")
            return

        elif password != verify:
            self.signup_statusLabel.configure(text="Passwords do not match.")
            return

        # Thank you https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/
        bytes = password.encode('utf-8')

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes, salt)

        conn = sqlite3.connect("sudoku.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Users ( 
                UserID INTEGER PRIMARY KEY AUTOINCREMENT, 
                AccountName TEXT NOT NULL UNIQUE,
                Salt BLOB NOT NULL, 
                HashedPassword BLOB NOT NULL, 
                CreatedAt TIMESTAMP DEFAULT (unixepoch())
            );
        """) # Thank you https://stackoverflow.com/questions/11556546/sqlite-storing-default-timestamp-as-unixepoch

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Users (AccountName, Salt, HashedPassword) VALUES (?, ?, ?)
            """, (name, salt, hashed))
        except sqlite3.IntegrityError:
            self.signup_statusLabel.configure(text="This account name is already taken.")
        except sqlite3.Error:
            self.signup_statusLabel.configure(text="An unexpected error occurred.")

        conn.commit()
        
        id = cursor.lastrowid    
        self.setIdCommand(id)
        self.accountsPageCommand()

        conn.close()
        

class AccountError(Exception):
    pass