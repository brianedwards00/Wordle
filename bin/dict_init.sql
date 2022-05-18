-- $ sqlite3 dict.db < dict_init.sql

BEGIN TRANSACTION;
DROP TABLE IF EXISTS dict;
CREATE TABLE dict (
    id INTEGER PRIMARY KEY,
    word TEXT,
    UNIQUE(word)
);
COMMIT;
