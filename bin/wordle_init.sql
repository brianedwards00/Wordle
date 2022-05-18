-- $ sqlite3 wordle.db < wordle_init.sql

BEGIN TRANSACTION;
DROP TABLE IF EXISTS wordle;
CREATE TABLE wordle (
    id INTEGER PRIMARY KEY,
    answer TEXT,
    answer_date TEXT,
    UNIQUE(answer, answer_date)
);
COMMIT;
