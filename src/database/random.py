import pandas as pd
import sqlite3

conn = sqlite3.connect("sudoku.db")

df = pd.read_sql_query("""
    SELECT P.SerialisedBoard, P.Difficulty, PT.Tag
    FROM Puzzles P
    INNER JOIN PuzzleTags PT
        ON PT.PuzzleID = P.PuzzleID
    GROUP BY P.PuzzleID
    ORDER BY P.Difficulty DESC
""", conn)
print(df.head(10))