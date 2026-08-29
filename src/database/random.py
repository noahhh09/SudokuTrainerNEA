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

# df = pd.read_sql_query("""
#     SELECT COUNT(*)
#     FROM PuzzleTags
#     WHERE Tag = 'NakedTriple'
# """, conn)
# print(df)

findString: str = "x42f4f3fx18f/x36fx21fx2/6f5fx17fx5/1fx36fx4/x18fx25f2f6fx2/x31fx32fx1/x27f3fx15f9fx2/x19fx58fx1/x11fx24fx35f"
df = pd.read_sql_query("""
    SELECT P.SerialisedBoard, P.difficulty
    FROM Puzzles P
    ORDER BY P.difficulty DESC
    LIMIT 5
""", conn)
for n in range(5):
    print(df["SerialisedBoard"].iloc[n], df["difficulty"].iloc[n])
