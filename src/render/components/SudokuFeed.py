from typing import Any

import customtkinter as ctk

from src.analysis import ALL_TECHNIQUES, Contradictions
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState


class SudokuFeed(ctk.CTkFrame):
    def __init__(self, master: Any, firstState: BoardState):
        super().__init__(master)

        self.grid_rowconfigure(1, weight=1)

        titleFont = ctk.CTkFont(size=24, weight="bold")
        titleLabel = ctk.CTkLabel(self, text="Feed", font=titleFont)
        titleLabel.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.feedFrame = ctk.CTkScrollableFrame(self, width=500)
        self.feedFrame.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")
        self.feedFrame.columnconfigure(0, weight=1) # Allows the feed widgets to take up the frames full width.

        self.feedWidgets: list[ctk.CTkBaseClass] = []

        self.repopulate(firstState)

    def repopulate(self, board: BoardState):
        for widget in self.feedWidgets:
            widget.destroy()
        
        contradictions = Contradictions.detectContradictions(board)
        for contra in contradictions:
            widget = ContradictionWidget(self.feedFrame, contra)
            widget.grid(row=len(self.feedWidgets), sticky="ew", pady=(0 if len(self.feedWidgets) == 0 else 5, 0))
            self.feedWidgets.append(widget)

        for techniqueType in ALL_TECHNIQUE_TYPES:
            techniques = techniqueType.findAvailable(board)
            print(techniqueType.__name__, len(techniques), techniques)
            print("")


class ContradictionWidget(ctk.CTkFrame):
    def __init__(self, master: Any, contra: Contradictions.Contradiction):
        super().__init__(master, border_width=2, border_color="#ee0000")

        contraFont = ctk.CTkFont(size=16, weight="bold")

        titleLabel = ctk.CTkLabel(self, text="Contradiction", font=contraFont)
        titleLabel.grid(row=0, column=0, sticky="w", padx=2, pady=2)

        description = ctk.CTkLabel(self, text=f"There are {len(contra.cellsInvolved)} of the digit {contra.value} in {contra.unitType.name} {contra.unitIndex + 1}")
        description.grid(row=1, column=0, sticky="w", padx=2, pady=2)