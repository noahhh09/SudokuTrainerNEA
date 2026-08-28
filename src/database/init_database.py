# Used to generate database tags and reformat the Kaggle 3 million dataset.
# https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings
# Requires 'sudoku-3m.csv' file in this directory.

# Applying tags takes quite a while. Approx 30 seconds per 25,000 tags with Naked + Hidden singles.
# Set to -1 to load all from dataset.
LOAD_MAX = 100000
# Tagging takes ages.
NUM_TAGGED = 100000

import json
import time
from pathlib import Path

import pandas as pd
import sqlite3

from src.analysis import ALL_TECHNIQUES
from src.core.BoardState import BoardState

global n
n = 0

def convertPuzzleString(puzzle: str):
    result = ""
    consequtiveZeroes = 0

    for i, char in enumerate(list(puzzle)):
        if i % 9 == 0 and i != 0:
            if consequtiveZeroes > 0:
                result += "x" + str(consequtiveZeroes)

            consequtiveZeroes = 0
            result += "/"

        if char == ".":
            consequtiveZeroes += 1
        else:
            if consequtiveZeroes > 0:
                result += "x" + str(consequtiveZeroes)
                consequtiveZeroes = 0

            result += char + "f"

    if consequtiveZeroes > 0:
        result += "x" + str(consequtiveZeroes)
        consequtiveZeroes = 0

    global n
    n += 1
    if n % 100 == 0:
        print(f"\r    Converted {n} BoardStrings", end="", flush=True)
    
    return result

def applyTags(row):
    boardState = BoardState.deserialise(row["SerialisedBoard"])
    techniques = ALL_TECHNIQUES

    tags = []

    for technique in techniques:
        if len(technique.findAvailable(boardState,findFirstOnly=False)) >= 1:
            tags.append(technique.__name__)

    global n
    global t
    n += 1
    if n % 250 == 0:
        now = time.time()
        delta = now - t
        avg = delta / n
        projected = (NUM_TAGGED - n) * avg
        percent = (n / NUM_TAGGED) * 100
        print(f"\r    Tagged {n} boards ({percent:.2f}%) ({delta:.1f}s; avg {avg:.6f}s; projected {projected:.1f}s)", end="", flush=True)

    return tags

path = Path(__file__).parent / "sudoku-3m.csv"

print("Loading df...")
df = pd.read_csv(path, usecols=["id", "puzzle", "clues", "difficulty"], nrows=(None if LOAD_MAX <= 0 else LOAD_MAX)).rename(columns={"id": "PuzzleID", "puzzle": "SerialisedBoard"})
print(f"Loaded {len(df.index)} dataframe rows. Converting puzzle strings...")
df['SerialisedBoard'] = df['SerialisedBoard'].apply(lambda x:convertPuzzleString(x))
print()
print("Converted puzzle strings. Storing puzzles...")

conn = sqlite3.connect("sudoku.db")

df.to_sql(
    "Puzzles",
    conn,
    if_exists="replace",
    index=False
)
print("Stored puzzles.")

global t
n = 0
t = time.time()
tags_df = df[["PuzzleID", "SerialisedBoard"]]

print(f"Tagging first {NUM_TAGGED if NUM_TAGGED > 0 else len(tags_df.index)} puzzles.")
tags_df["Tag"] = tags_df.head(NUM_TAGGED if NUM_TAGGED > 0 else len(tags_df.index)).apply(
    lambda row: applyTags(row),
    axis=1
)
tags_df = tags_df.explode("Tag")

print()
print("Applied tags.")
print(f"Storing {n} tagged Puzzles")
tags_df[["PuzzleID", "Tag"]].to_sql(
    "PuzzleTags",
    conn,
    if_exists="replace",
    index=False
)

conn.close()