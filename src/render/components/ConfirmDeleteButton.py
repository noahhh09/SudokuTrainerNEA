from customtkinter import CTkButton

# Sourced from a personal project I did a while back.
class ConfirmDeleteButton(CTkButton):
    def __init__(self, parent, command, **kwargs):
        self.awaiting_confirmation = False
        self.command = command

        super().__init__(parent, command=self.on_click, **kwargs)
        self.nonAwaitingText = self._text

    def on_click(self):
        if self.awaiting_confirmation:
            self.command()
        else:
            self.configure(text="Confirm")
            self.awaiting_confirmation = True
            self.after(5000, self.reset_button)

    def reset_button(self):
        if self.awaiting_confirmation:
            self.configure(text=self.nonAwaitingText)
            self.awaiting_confirmation = False
