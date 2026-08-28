import customtkinter as ctk

from src.analysis.Technique import ALL_TECHNIQUES, Technique

class TechniquesLibraryPage(ctk.CTkFrame):
    def __init__(self, master, mainMenuCommand, **kwargs):
        super().__init__(master, **kwargs)

        self.mainMenuButton = ctk.CTkButton(self, text="Back to Main Menu", width=200, height=50, command=mainMenuCommand)
        self.mainMenuButton.place(relx=0.01, rely=0.05, anchor="w")

        self.techniquesGrid = ctk.CTkScrollableFrame(self)

        for i, technique in enumerate(ALL_TECHNIQUES):
            widget = TechniqueWidget(self.techniquesGrid, technique=technique)
            widget.grid(column=i % 4, row=i // 4, padx=(0 if i % 4 == 0 else 5, 5), pady=(5, 5))

        self.techniquesGrid.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.8, anchor="n")


class TechniqueWidget(ctk.CTkFrame):
    def __init__(self, master, technique: type[Technique], **kwargs): # I just want to say the type[Technique] thing is my coolest discovery yet.
        super().__init__(master, height=300, **kwargs)

        self.nameLabel = ctk.CTkLabel(self, text=technique.displayName, font=ctk.CTkFont(size=24, weight="bold"))
        self.nameLabel.place(relx=0.5, rely=0.1, relwidth=1, anchor="n")

        self.descriptionLabel = ctk.CTkLabel(self, text=technique.description, wraplength=168, font=ctk.CTkFont(size=14))
        self.descriptionLabel.place(relx=0.5, rely=0.3, anchor="n")

        self.explainButton = ctk.CTkButton(self, text="Learn")
        self.explainButton.place(relx=0.5, rely=0.8, anchor="center")

        self.practiceButton = ctk.CTkButton(self, text="Practice")
        self.practiceButton.place(relx=0.5, rely=0.9, anchor="center")
