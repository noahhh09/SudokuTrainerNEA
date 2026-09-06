# ChatGPT Generated @ https://chatgpt.com/share/6a985ab9-2390-83eb-bd36-02f36c95f836
# Purely to test SQL

import sqlite3

conn = sqlite3.connect("sudoku.db")

while True:
    try:
        cmd = input("sqlite> ").strip()

        if cmd.lower() in {"exit", "quit"}:
            break

        cursor = conn.execute(cmd)

        if cursor.description is not None:
            # SELECT-like query
            rows = cursor.fetchall()

            # Column headings
            print(" | ".join(column[0] for column in cursor.description))
            print("-" * 50)

            for row in rows:
                print(" | ".join(str(value) for value in row))

        else:
            # INSERT / UPDATE / DELETE / CREATE etc.
            conn.commit()
            print(f"Done. {cursor.rowcount} row(s) affected.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

conn.close()