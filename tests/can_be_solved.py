import sqlite3
import time

from src.analysis import ALL_TECHNIQUE_TYPES
from src.analysis.techniques.XWing import XWing
from src.core.BoardState import BoardState

def boards_match(board1: BoardState, board2: BoardState) -> bool:
    for i in range(9):
        for j in range(9):
            if board1.getCell(i, j).getValue() != board2.getCell(i, j).getValue():
                return False

    return True

conn = sqlite3.connect("sudoku.db")
cur = conn.cursor()
cur = cur.execute("""
    SELECT PuzzleID, SerialisedBoard, solution, difficulty
    FROM Puzzles
    WHERE difficulty > 0
    ORDER BY difficulty ASC
    LIMIT 20000
""")

puzzles = cur.fetchall()
highest_solved_difficulty: float = -1
highest_solved_diff_id: int = -1

size = len(puzzles)
evaluated = 0
solved = 0
t = time.perf_counter()

for id, puzzle, solution, difficulty in puzzles:
    solvedBoard = BoardState.deserialise(solution)
    board = BoardState.deserialise(puzzle)

    x_wing = False
    while not boards_match(board, solvedBoard):
        changed = False
        for tech in ALL_TECHNIQUE_TYPES:
            found = tech.findAvailable(board)
            if len(found) > 0:
                technique = found[0]
                for move in technique.moves:
                    move.apply(board)

                if tech is XWing:
                    x_wing = True

                changed = True
                break

        if not changed:
            break

    delta = time.perf_counter() - t
    evaluated += 1
    avg = delta / evaluated
    microseconds = int(avg * 1e6)
    projected = (size - evaluated) * avg

    if boards_match(board, solvedBoard):
        if x_wing:
            print(f"\r\033[KSolvable with X-Wing: {id}", end="\n", flush=True)

        if difficulty > highest_solved_difficulty:
            highest_solved_difficulty = difficulty
            highest_solved_diff_id = id
            print(f"\r\033[KNew highest solved difficulty: {highest_solved_difficulty} (ID: {highest_solved_diff_id})", end="\n", flush=True)

        solved += 1


    print(f"\r\033[KEvaluated {evaluated} / {size} puzzles (of total, solved {(solved * 100) // evaluated}%) (avg {microseconds}μs) ({(evaluated * 100) // size}%) (projected {int(projected)}s)", end="", flush=True)

print(f"\r\033[KHighest solved difficulty: {highest_solved_difficulty} (ID: {highest_solved_diff_id})")


