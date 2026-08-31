from typing import Any

import customtkinter as ctk

from src.analysis import ALL_TECHNIQUE_TYPES, Contradictions
from src.analysis.Technique import Technique
from src.core.BoardState import BoardState


class SudokuFeed(ctk.CTkFrame):
    def __init__(self, master: Any, firstState: BoardState, applyCommand):
        super().__init__(master, corner_radius=0, border_width=2)
        self.board = firstState
        self.applyCommand = applyCommand

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        titleFont = ctk.CTkFont(size=24, weight="bold")
        titleLabel = ctk.CTkLabel(self, text="Feed", font=titleFont)
        titleLabel.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.feedFrame = ctk.CTkScrollableFrame(self, width=500)
        self.feedFrame.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")
        self.feedFrame.columnconfigure(0, weight=1) # Allows the feed widgets to take up the frames full width.

        self.feedWidgets: list[ctk.CTkBaseClass] = []
        self.revealedHintProperties: dict[str, list[str]] = {} # Dict of {technique identity: revealed parameters}

        self.repopulate(firstState)

    def repopulate(self, board: BoardState):
        self.board = board

        for widget in self.feedWidgets:
            widget.destroy()
        
        contradictions = Contradictions.detectContradictions(board)
        for contra in contradictions:
            widget = ContradictionWidget(self.feedFrame, contra)
            widget.grid(row=len(self.feedWidgets), sticky="ew", pady=(0 if len(self.feedWidgets) == 0 else 10, 0))
            self.feedWidgets.append(widget)

        for techniqueType in ALL_TECHNIQUE_TYPES:
            techniques = techniqueType.findAvailable(board)

            for instance in techniques:
                identity = instance.identity()
                if identity in self.revealedHintProperties:
                    widget = HintWidget(self.feedFrame, instance, revealCommand=self.revealHintProperty, applyCommand=self.applyCommand, discardCommand=self.discardHint, revealed=self.revealedHintProperties[identity])
                    widget.grid(row=len(self.feedWidgets), sticky="ew", pady=(0 if len(self.feedWidgets) == 0 else 5, 0))
                    self.feedWidgets.append(widget)

    def addHint(self, technique: Technique, reveal: list[str] = []) -> bool:
        identity = technique.identity()
        if identity in self.revealedHintProperties:
            return False

        self.revealedHintProperties[identity] = reveal
        self.repopulate(self.board)
        return True

    def discardHint(self, technique: Technique):
        identity = technique.identity()
        if identity in self.revealedHintProperties:
            del self.revealedHintProperties[identity]

        self.repopulate(self.board)

    def revealHintProperty(self, techniqueIdentity: str, propertyName: str):
        revealed = self.revealedHintProperties[techniqueIdentity] if techniqueIdentity in self.revealedHintProperties else []
        if propertyName not in revealed:
            revealed.append(propertyName)
        else:
            raise ValueError(f"Property {propertyName} already revealed.")

        self.repopulate(self.board)


class ContradictionWidget(ctk.CTkFrame):
    def __init__(self, master: Any, contra: Contradictions.Contradiction):
        super().__init__(master, border_width=2, border_color="#ee0000")

        titleFont = ctk.CTkFont(size=16, weight="bold")
        titleLabel = ctk.CTkLabel(self, text="Contradiction", font=titleFont)
        titleLabel.grid(row=0, column=0, sticky="w", padx=2, pady=2)

        description = ctk.CTkLabel(self, text=f"There are {len(contra.cellsInvolved)} of the digit {contra.value} in {contra.unitType.name} {contra.unitIndex + 1}")
        description.grid(row=1, column=0, sticky="w", padx=2, pady=2)


class HintWidget(ctk.CTkFrame):
    def __init__(self, master: Any, technique: Technique, revealCommand, discardCommand, applyCommand, revealed: list[str] = []):
        super().__init__(master, border_width=2)
        self.technique = technique
        identity = technique.identity()

        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)

        titleFont = ctk.CTkFont(size=16, weight="bold")
        titleLabel = ctk.CTkLabel(self, text="Hint", font=titleFont)
        titleLabel.grid(row=0, column=0, sticky="w", padx=(5,0), pady=5)

        clearButton = ctk.CTkButton(self, text="Discard", fg_color="#ff0000", command=lambda: discardCommand(technique))
        clearButton.grid(row=0, column=1, sticky="e", padx=(0,5), pady=5)
        
        hintData = {"Technique Type": technique.__class__.displayName, **technique.getHintData()}
        for i, key in enumerate(hintData):
            value = hintData[key]

            titleLabel = ctk.CTkLabel(self, text=key)
            titleLabel.grid(row=i + 1, column=0, sticky="w", padx=(5,0), pady=3)

            if key in revealed:
                answerLabel = ctk.CTkLabel(self, text=value)
                answerLabel.grid(row=i + 1, column=1, sticky="e", padx=(0,5), pady=3)
            else:
                revealButton = ctk.CTkButton(self, text=f"Reveal {key}", command=lambda key=key: revealCommand(identity, key))
                revealButton.grid(row=i + 1, column=1, sticky="e", padx=(0,5), pady=3)

        applyButton = ctk.CTkButton(self, text="Apply", fg_color="#ff0000", command=lambda technique=technique: applyCommand(technique))
        applyButton.grid(row=len(hintData) + 1, column=0, sticky="e", columnspan=2, padx=(0,5), pady=3)