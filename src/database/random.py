import pandas as pd
import sqlite3

from src.analysis.techniques.NakedGroup import NakedTriple
from src.core.BoardState import BoardState

conn = sqlite3.connect("sudoku.db")

# df = pd.read_sql_query("""
#     SELECT P.PuzzleID, P.SerialisedBoard, P.Difficulty, PT.Tag
#     FROM Puzzles P
#     INNER JOIN PuzzleTags PT
#         ON PT.PuzzleID = P.PuzzleID
#     GROUP BY P.PuzzleID
#     HAVING COUNT(*) = 1
#         AND MAX(PT.Tag) = 'NakedTriple'
# """, conn)
# print(df["SerialisedBoard"].iloc[0])

# board = BoardState.deserialise(df["SerialisedBoard"].iloc[0])
# print(NakedTriple.findAvailable(board))

df = pd.read_sql_query("""
    SELECT COUNT(*)
    FROM PuzzleTags
    WHERE Tag = 'NakedTriple'
""", conn)
print(df)
