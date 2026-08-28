from typing import Tuple
from src.analysis import BoardUtils
from src.analysis.Technique import HiddenSingle
from src.core.BoardState import BoardState
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
                loadBoardStateCommand=self.loadBoardStatePuzzle,
                techniquesPageCommand=self.techniquesPage,
                accountsPageCommand=self.accountsPage
            )
        )

    def newPuzzle(self):
        self.__setPage(
            SudokuPage(
                self,
                BoardState.deserialise("1fx25fx13f7fx2/6fx13fx28fx19fx1/x59f8fx2/x11fx7/8f7f6f1fx5/x56fx3/x87f/x18fx19fx17f6fx14f/7fx36fx13f1f2f"),
                mainMenuCommand=self.mainMenu
            )
        )

    def loadBoardStatePuzzle(self, boardState: BoardState):
        boardState = BoardUtils.copyAndPopulateCandidates(boardState)

        self.__setPage(
            SudokuPage(
                self,
                boardState,
                mainMenuCommand=self.mainMenu
            )
        )
        
    def techniquesPage(self):
        self.__setPage(
            TechniquesLibraryPage(
                self,
                mainMenuCommand=self.mainMenu,
                loadBoardStateCommand=self.loadBoardStatePuzzle
            )
        )

    def accountsPage(self):
        pass