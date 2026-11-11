# SudokuTrainerNEA
## Setup & Running
Before running the app before its first use, please set up the database as instructed below.

To execute the program, type `python -m main` into command prompt from the root directory.

## Database Setup
1. Download the dataset from https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings and save it in the "/src/database/" directory as 'sudoku-3m.csv'
2. Run `python -m src.database.init_database` and wait for it to finish. 
> *This command defaults to populating 1000 puzzles. Specify a number at the end of the command to use a custom amount (e.g. `python -m src.database.init_database 500` to populate 500 puzzles).*