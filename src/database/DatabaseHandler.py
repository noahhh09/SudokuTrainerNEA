import sqlite3

from src.core.BoardState import BoardState
from src.core.Move import CandidateChangeMove, EliminationChangeMove, Move, ValueChangeMove

VALUE_CHANGE_IDENTIFIER = "VALUE_CHANGE_MOVE"
CANDIDATE_CHANGE_IDENTIFIER = "CANDIDATE_CHANGE_MOVE"
ELIMINATION_CHANGE_IDENTIFER = "ELIMINATION_CHANGE_MOVE"

typeToId = {
    ValueChangeMove: "VALUE_CHANGE_MOVE",
    CandidateChangeMove: "CANDIDATE_CHANGE_MOVE",
    EliminationChangeMove: "ELIMINATION_CHANGE_MOVE"
}
idToType = {v: k for k, v in typeToId.items()}

def createGameFromPuzzle(profileId: int, puzzleId: int) -> int:
    """Returns the game ID of the created game instance."""

    conn = sqlite3.connect("sudoku.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Games (ProfileID, PuzzleID)
        VALUES (?, ?)
    """, (profileId, puzzleId))

    # Thank you https://stackoverflow.com/questions/69287294/how-can-i-capture-the-rowid-of-newly-inserted-row-in-sqlite-flask
    id = cur.lastrowid

    if id is None:
        raise TypeError("Provided ID of game instance is None. See insertNewPuzzle() in DatabaseUtils.py")

    conn.commit()
    conn.close()

    return id

def getInitialStateFromGame(gameId: int) -> tuple[BoardState, int]:
    """Returns (currentState, solutionState, puzzleId)"""

    conn = sqlite3.connect("sudoku.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT SerialisedBoard, Puzzles.PuzzleID
        FROM Puzzles
        INNER JOIN Games
            ON Games.PuzzleID = Puzzles.PuzzleID
        WHERE Games.GameID = ?
    """, (gameId,))

    initialStateStr, puzzleId = cur.fetchone()
    state = BoardState.deserialise(initialStateStr)

    return state, puzzleId

def getMovesFromGame(gameId: int) -> list[Move]:
    conn = sqlite3.connect("sudoku.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT RowNum, ColNum, MoveType, MoveData
        FROM Moves
        WHERE GameID = ?
        ORDER BY MoveNumber ASC
    """, (gameId,))

    serialisedMoves = cur.fetchall()
    print(serialisedMoves)
    result = []
    for row, col, moveType, moveData in serialisedMoves:
        moveType = _deserialiseMoveType(moveType)
        move = _deserialiseMove(moveType, row, col, moveData)
        if move is not None:
            result.append(move)

    return result

def addMoveToGame(gameId: int, move: Move):
    type = _getMoveType(move)
    extraData = _serialiseMoveData(move)

    conn = sqlite3.connect("sudoku.db")
    cur = conn.cursor()

    cur.execute("SELECT MAX(MoveNumber) FROM Moves WHERE GameID = ?", (gameId,))
    moveNumber = cur.fetchone()[0]
    if moveNumber is None:
        moveNumber = 0
    moveNumber += 1

    cur.execute("""
        INSERT INTO Moves (GameID, MoveNumber, RowNum, ColNum, MoveType, MoveData)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (gameId, moveNumber, move.row, move.col, type, extraData))

    conn.commit()
    conn.close()

def _getMoveType(move: Move):
    return typeToId[type(move)]

def _serialiseMoveData(move: Move):
    if type(move) is ValueChangeMove:
        return f"{move.newValue};{move.oldValue};{",".join([f"{row}{col}" for row, col in move.removedCandidatePositions])}"
    elif type(move) is CandidateChangeMove or type(move) is EliminationChangeMove:
        return f"{move.candidateNumber};{move.add}"

def _deserialiseMoveType(serialised: str) -> type[Move]:
    return idToType[serialised]

def _deserialiseMove(moveType: type[Move], row: int, col: int, serialisedData: str) -> Move | None:
    if moveType is ValueChangeMove:
        newValue, oldValue, removedPositionsStr = serialisedData.split(";")
        removedPositions = []
        if len(removedPositionsStr) > 0:
            removedPositions = [(int(x[0]), int(x[1])) for x in removedPositionsStr.split(",")]

        if newValue == "None":
            newValue = None
        else:
            newValue = int(newValue)

        if oldValue == "None":
            oldValue = None
        else:
            oldValue = int(oldValue)

        return ValueChangeMove(row, col, newValue, oldValue, removedPositions)

    elif moveType is EliminationChangeMove or moveType is CandidateChangeMove:
        candidateNumber, add = serialisedData.split(";")
        return moveType(row, col, int(candidateNumber), bool(add))

def removeMoveNumbersGreaterThan(gameId: int, x: int):
    conn = sqlite3.connect("sudoku.db")
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM Moves
        WHERE GameID = ?
        AND MoveNumber > ?
    """, (gameId, x))

    conn.commit()
    conn.close()