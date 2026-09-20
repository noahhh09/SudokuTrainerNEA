import random
from typing import Any

import customtkinter as ctk

from src.analysis import ALL_TECHNIQUE_TYPES
from src.analysis.Technique import Technique

SPECIFIC_TECHNIQUES_SHOWN = 3

class SudokuHintMenu(ctk.CTkFrame):
    def __init__(self, master: Any, getBoardCommand, askHintCommand):
        super().__init__(master, corner_radius=0, border_width=2)

        self.getBoardCommand = getBoardCommand
        self.askHintCommand = askHintCommand

        titleFont = ctk.CTkFont(size=24, weight="bold")
        titleLabel = ctk.CTkLabel(self, text="Hints", font=titleFont)
        titleLabel.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="ew", columnspan=2 + SPECIFIC_TECHNIQUES_SHOWN)

        statusFont = ctk.CTkFont(size=12)
        self.statusLabel = ctk.CTkLabel(self, height=1, text="", font=statusFont, text_color="#ff0000")
        self.statusLabel.grid(row=1, column=0, padx=5, sticky="ew", columnspan=2 + SPECIFIC_TECHNIQUES_SHOWN)

        randomButton = ctk.CTkButton(self, text="Random", command=self._askRandom)
        randomButton.grid(row=2, column=0, padx=5, pady=5, columnspan=2 + SPECIFIC_TECHNIQUES_SHOWN)

        self.specificTechniqueIdx = 0
        leftButton = ctk.CTkButton(self, width=28, text="<", command=lambda: self._gridSpecificTechniquesFrom(max(0, self.specificTechniqueIdx - SPECIFIC_TECHNIQUES_SHOWN)))
        leftButton.grid(row=3, column=0, padx=5, sticky="e", pady=5)

        self.specificTechniqueButtons: list[ctk.CTkBaseClass] = []
        for techType in ALL_TECHNIQUE_TYPES:
            button = ctk.CTkButton(self, text=techType.displayName, command=lambda techType=techType: self._askSpecific(techType))
            self.specificTechniqueButtons.append(button)

        rightButton = ctk.CTkButton(self, width=28, text=">", command=lambda: self._gridSpecificTechniquesFrom(min(self.specificTechniqueIdx + SPECIFIC_TECHNIQUES_SHOWN, len(self.specificTechniqueButtons) - SPECIFIC_TECHNIQUES_SHOWN)))
        rightButton.grid(row=3, column=SPECIFIC_TECHNIQUES_SHOWN + 1, padx=5, pady=5)

        self._gridSpecificTechniquesFrom(0)

    def _gridSpecificTechniquesFrom(self, startIdx: int):
        self.specificTechniqueIdx = startIdx

        for i, button in enumerate(self.specificTechniqueButtons):
            if i < startIdx or i >= startIdx + SPECIFIC_TECHNIQUES_SHOWN:
                button.grid_forget()
                continue

            col = i - startIdx
            button.grid(row=3, column=col + 1, padx=1, pady=5)

    def _askRandom(self):
        board = self.getBoardCommand()

        found: list[Technique] = []
        
        for techType in ALL_TECHNIQUE_TYPES:
            available = techType.findAvailable(board)
            for technique in available:
                found.append(technique)

        self._sendRandomFromList(found)

    def _askSpecific(self, techType: type[Technique]):
        board = self.getBoardCommand()
                
        available = techType.findAvailable(board)
        self._sendRandomFromList(available, reveal=True)

    def _sendRandomFromList(self, list: list[Technique], reveal: bool = False):
        self.statusLabel.configure(text="")
        
        if len(list) == 0:
            self.statusLabel.configure(text="No available hints to be given.")

        added = False
        while not added and len(list) > 0:
            selected = random.choice(list)
            list.remove(selected)

            added = self.askHintCommand(selected, reveal=["Technique Type"] if reveal else [])

        if not added:
            self.statusLabel.configure(text="Could not find any new hints not already given.")

        
