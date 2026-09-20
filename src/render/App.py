from typing import Tuple
from src.analysis import BoardUtils
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState
from src.render.pages.AccountsPageLoggedIn import AccountsPageLoggedIn
from src.render.pages.AccountsPageLoggedOut import AccountsPageLoggedOut
from src.render.pages.MainMenuPage import MainMenuPage
from src.render.pages.SudokuPage import SudokuPage
from src.render.pages.TechniqueLearningPage import TechniqueLearningPage
from src.render.pages.TechniquesLibraryPage import TechniquesLibraryPage

import customtkinter as ctk

RATIO = 720 / 1280
WIDTH = 1440


class App(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.profileId: int | None = None

        self.title("Sudoku Trainer")
        self.geometry(f"{WIDTH}x{(WIDTH * RATIO) // 1}")

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
                profileId=self.profileId,
                loadBoardStateCommand=self.loadBoardStatePuzzle,
                techniquesPageCommand=self.techniquesPage,
                accountsPageCommand=self.accountsPage
            )
        )

    def loadBoardStatePuzzle(self, boardState: BoardState):
        # boardState = BoardUtils.copyAndPopulateCandidates(boardState)

        self.__setPage(
            SudokuPage(
                self,
                boardState,
                mainMenuCommand=self.mainMenu
            )
        )

    def learnSpecificTechnique(self, type: type[Technique]):
        self.__setPage(
            TechniqueLearningPage(
                self,
                type,
                mainMenuCommand=self.mainMenu,
            )
        )
        
    def techniquesPage(self):
        self.__setPage(
            TechniquesLibraryPage(
                self,
                mainMenuCommand=self.mainMenu,
                loadBoardStateCommand=self.loadBoardStatePuzzle,
                techniquePageCommand=self.learnSpecificTechnique
            )
        )

    def accountsPage(self):
        if self.profileId is None:
            self.__setPage(
                AccountsPageLoggedOut(
                    self,
                    mainMenuCommand=self.mainMenu,
                    setIdCommand=self.setProfileId,
                    accountsPageCommand=self.accountsPage
                )
            )
        else:
            self.__setPage(
                AccountsPageLoggedIn(
                    self,
                    profileId=self.profileId,
                    mainMenuCommand=self.mainMenu,
                    accountsPageCommand=self.accountsPage
                )
            )

    def setProfileId(self, id):
        self.profileId = id