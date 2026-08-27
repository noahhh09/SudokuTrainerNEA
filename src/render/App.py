from typing import Tuple
from src.render.pages.MainMenuPage import MainMenuPage
from src.render.pages.SudokuPage import SudokuPage
from src.render.pages.TechniquesLibraryPage import TechniquesLibraryPage

import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Sudoku Trainer")
        self.geometry("1280x720")

        self.page: ctk.CTkFrame | None = None

        self.mainMenu()

    def __setPage(self, page: ctk.CTkFrame):
        if self.page is not None:
            self.page.destroy()

        self.page = page
        self.page.pack(fill="both", expand=True)

    def mainMenu(self):
        self.__setPage(
            MainMenuPage(
                self,
                newPuzzleCommand=self.newPuzzle,
                techniquesPageCommand=self.techniquesPage,
                accountsPageCommand=self.accountsPage
            )
        )

    def newPuzzle(self):
        self.__setPage(
            SudokuPage(
                self,
                mainMenuCommand=self.mainMenu
            )
        )

    def techniquesPage(self):
        self.__setPage(
            TechniquesLibraryPage(
                self,
                mainMenuCommand=self.mainMenu
            )
        )

    def accountsPage(self):
        pass