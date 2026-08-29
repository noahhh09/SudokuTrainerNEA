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

        self.techniquesFrame = ctk.CTkScrollableFrame(self, width=500)
        self.techniquesFrame.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")

        self.repopulate(firstState)

    def repopulate(self, board: BoardState):
        widgetCount = 0

        contradictions = Contradictions.detectContradictions(board)
        for contra in contradictions:
            widget = ContradictionWidget(self.techniquesFrame, contra)
            widget.grid(row=widgetCount, sticky="ew", pady=(0 if widgetCount == 0 else 5, 0))
            widgetCount += 1

        for tech in ALL_TECHNIQUES:
            available = tech.findAvailable(board)
            print(tech.__name__, len(available), available)
            print("")


class ContradictionWidget(ctk.CTkFrame):
    def __init__(self, master: Any, contra: Contradictions.Contradiction):
        super().__init__(master, border_width=2)

        titleLabel = ctk.CTkLabel(self, text="Contradiction")
        titleLabel.grid(row=0, column=0, sticky="w", padx=2, pady=2)

        description = ctk.CTkLabel(self, text=f"There are {len(contra.cellsInvolved)} {contra.value}s in {contra.unitType.name} {contra.unitIndex + 1}")
        description.grid(row=1, column=0, sticky="w", padx=2, pady=2)