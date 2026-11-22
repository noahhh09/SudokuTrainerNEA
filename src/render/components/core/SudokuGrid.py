from typing import Any

import customtkinter as ctk
import tkinter as tk

from src.analysis import BoardUtils, Contradictions
from src.core.BoardState import BoardState
from src.core.Cell import Cell

# TODO: Move to constants file.
DEFAULT_HIGHLIGHT = "white"
CONTRADICTION_HIGHLIGHT = "#ff0000"
INCONSISTENCY_HIGHLIGHT = "#ff7700"
SELECTED_HIGHLIGHT = "#2761ff"
SIMILAR_CELL_SELECTED_HIGHLIGHT = "#507eff"

EDITABLE_COLOUR = "#1111ff"
UNEDITABLE_COLOUR = "#000000"

CANDIDATE_COLOUR = "#444444"
ELIMINATION_COLOUR = "#ff0000"

class SudokuGrid(ctk.CTkFrame):
    def __init__(self, master: Any, boardState: BoardState, solution: BoardState | None = None, width: int = 640, height: int = 640, **kwargs):
        super().__init__(master, width, height, fg_color="black", **kwargs)

        self.boardState = boardState
        self.solution = solution
        self.sudokuCells: list[list[SudokuCell]] = []
        self.selectedCellPosition: tuple[int, int] | tuple[None, None] = (None, None)
        self.selectedDigit: int | None = None

        for i in range(9):
            row: list[SudokuCell] = []

            for j in range(9):
                cell = SudokuCell(self, i, j, boardState.getCell(i, j), self.selectCell)

                leftpad = 5 if (j % 3 == 0 and j != 0) else 1
                toppad = 5 if (i % 3 == 0 and i != 0) else 1

                cell.grid(row=i, column=j, padx=(leftpad, 1), pady=(toppad, 1))
                row.append(cell)

            self.sudokuCells.append(row)

        self.redraw()

    def highlightCells(self, cells: list[tuple[int, int]], colour: str):
        for row, col in cells:
            self.sudokuCells[row][col].highlight(colour)

    def selectCell(self, row, col):
        self.selectedCellPosition = (row, col)
        self.selectedDigit = self.boardState.getCell(row, col).getValue()
        for i in range(9):
            for j in range(9):
                self.sudokuCells[i][j].updateHighlightState(self.selectedCellPosition, self.selectedDigit)

    def redraw(self):
        self.updateInconsistenciesWithSolution()
        self.updateContradictions()

        for i in range(9):
            for j in range(9):
                self.sudokuCells[i][j].redraw(self.boardState.getCell(i, j))
                self.sudokuCells[i][j].updateHighlightState(self.selectedCellPosition, self.selectedDigit)


    def redrawCell(self, row: int, col: int):
        self.updateInconsistenciesWithSolution()
        self.updateContradictions()

        self.sudokuCells[row][col].redraw(self.boardState.getCell(row, col))
        self.sudokuCells[row][col].updateHighlightState(self.selectedCellPosition, self.selectedDigit)

    def updateContradictions(self):
        contradictions = Contradictions.detectContradictions(self.boardState)
        cellsWithContradictions: set[tuple[int, int]] = set()

        for contra in contradictions:
            cellsWithContradictions.update(contra.cellsInvolved)

        for i in range(9):
            for j in range(9):
                hasContra = (i, j) in cellsWithContradictions
                self.sudokuCells[i][j].isContradictory = hasContra
                    
    def updateInconsistenciesWithSolution(self):
        if self.solution is None:
            return

        for i in range(9):
            for j in range(9):
                cell = self.boardState.getCell(i, j)
                enteredValue = cell.getValue()
                if not cell.isEditable():
                    continue
                elif enteredValue is None:
                    self.sudokuCells[i][j].isInconsistentWithSolution = False # Only flag as contradictory if the user has inputted a value, and it is wrong.
                    continue

                solutionValue = self.solution.getCell(i, j).getValue()
                isContradictory = solutionValue != enteredValue 
                self.sudokuCells[i][j].isInconsistentWithSolution = isContradictory


class SudokuCell(ctk.CTkFrame):
    valueFont = None
    candidateFont = None
    eliminatedCandidateFont = None

    def __init__(self, master: Any, row: int, col: int, cell: Cell, onSelectCallback, size=64, **kwargs):
        super().__init__(master, width=size, height=size, **kwargs)

        self.isContradictory = False
        self.isInconsistentWithSolution = False

        self.row = row
        self.col = col
        self.cell = cell
        self.size = size

        self.onSelectCallback = onSelectCallback

        if SudokuCell.valueFont is None or SudokuCell.candidateFont is None:
            SudokuCell.valueFont = ctk.CTkFont(size=self.size // 3 + 8, weight='bold')
            SudokuCell.candidateFont = ctk.CTkFont(size=self.size // 8 + 4)
            SudokuCell.eliminatedCandidateFont = ctk.CTkFont(size=self.size // 8 + 4, overstrike=True)

        self.pack_propagate(False)

        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._onClick)

    def updateHighlightState(self, selectedPos: tuple[int, int] | tuple[None, None], selectedDigit: int | None):
        selectedRow, selectedCol = selectedPos
        similarCellSelected = False
        cellSelected = False
        value = self.cell.getValue()
        digitSelected = value is not None and selectedDigit == value
            
        if selectedRow is not None and selectedCol is not None:
            if selectedRow == self.row and selectedCol == self.col:
                cellSelected = True
            else:
                thisBlockIdx = BoardUtils.getBlockIndex(self.row, self.col)
                selectedBlockIdx = BoardUtils.getBlockIndex(selectedRow, selectedCol)
                
                similarCellSelected = (
                    thisBlockIdx == selectedBlockIdx or
                    self.row == selectedRow or
                    self.col == selectedCol
                )

        # Highest priority at the top.
        if self.isContradictory:
            self.highlight(CONTRADICTION_HIGHLIGHT)
        elif self.isInconsistentWithSolution:
            self.highlight(INCONSISTENCY_HIGHLIGHT)
        elif cellSelected:
            self.highlight(SELECTED_HIGHLIGHT)
        elif similarCellSelected or digitSelected:
            self.highlight(SIMILAR_CELL_SELECTED_HIGHLIGHT)
        else:
            self.highlight(DEFAULT_HIGHLIGHT) # Fallback to default. Used in case it was previously highlighted something else and no longer should be.

    def highlight(self, colour: str):
        self.canvas.configure(bg=colour)

    def _onClick(self, event):
        if self.onSelectCallback is not None:
            self.onSelectCallback(self.row, self.col)

    def redraw(self, cell: Cell | None = None):
        if cell is not None:
            self.cell = cell

        assert SudokuCell.valueFont
        assert SudokuCell.candidateFont
        assert SudokuCell.eliminatedCandidateFont

        self.canvas.delete("all")

        if self.cell.getValue() is not None:
            colour = UNEDITABLE_COLOUR if not self.cell.isEditable() else EDITABLE_COLOUR # O1.4. Non-editable cells should be clearly distinguishable from editable cells.
            self.canvas.create_text(self.size // 2, self.size // 2, text=str(self.cell.getValue()), font=SudokuCell.valueFont, tags="value", fill=colour)
        else:
            for candidate in self.cell.getEffectiveCandidates():
                row = (candidate - 1) // 3
                col = (candidate - 1) % 3

                self.canvas.create_text((col + 0.5) * (self.size / 3), (row + 0.5) * (self.size / 3), font=SudokuCell.candidateFont, text=candidate, tags="candidate", fill=CANDIDATE_COLOUR)

            for candidate in self.cell.getEliminatedCandidates():
                row = (candidate - 1) // 3
                col = (candidate - 1) % 3

                self.canvas.create_text((col + 0.5) * (self.size / 3), (row + 0.5) * (self.size / 3), font=SudokuCell.eliminatedCandidateFont, text=candidate, tags="candidate", fill=ELIMINATION_COLOUR)