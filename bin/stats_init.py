import sqlite3
import uuid

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: memoryview(u.bytes_le))

con = sqlite3.connect('./database/users.db', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (user_id GUID PRIMARY KEY, username VARCHAR UNIQUE);')


cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Alice"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Bob"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Carl"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Derek"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Earson"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Frank"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Greta"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Hank"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Ingrid"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Joe"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Karl"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Lam"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Melissa"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Nick"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Op"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Pris"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Quail"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Rick"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Steve"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Tuffy"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Under"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Vex"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Winner"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Xy"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Yes"])
cur.execute('INSERT INTO users VALUES (?,?)', [uuid.uuid4(), "Zetta"])
con.commit()

# Use the UUID's found here to set games for a specific user
cur.execute("SELECT * FROM users")

print(cur.fetchall())



con.commit()
con.close()


for r in range(1,4):
    con = sqlite3.connect(f'./database/games{r}.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS games;')
    cur.execute('DROP VIEW IF EXISTS wins;')
    cur.execute('DROP VIEW IF EXISTS streaks;')

    cur.execute('DROP TABLE IF EXISTS games;')
    cur.execute('CREATE TABLE games('
                        'user_id GUID NOT NULL,'
                        'game_id INTEGER NOT NULL,'
                        'finished DATE DEFAULT CURRENT_TIMESTAMP,'
                        'guesses INTEGER,'
                        'won BOOLEAN,'
                        'PRIMARY KEY(user_id, game_id));')

    cur.execute('CREATE VIEW wins AS '
                        'SELECT user_id,COUNT(won) '
                        'FROM games WHERE won =TRUE '
                        'GROUP BY user_id ORDER BY COUNT(won) DESC;')

    cur.execute('CREATE VIEW streaks '
                        'AS '
                            'WITH ranks AS ('
                                'SELECT DISTINCT '
                                    'user_id, '
                                    'finished, '
                                    'RANK() OVER(PARTITION BY user_id ORDER BY finished) AS rank '
                                'FROM '
                                    'games '
                                'WHERE '
                                    'won = TRUE '
                                'ORDER BY '
                                    'user_id, '
                                    'finished'
                            '), '
                        'groups AS ('
                            'SELECT '
                                'user_id, '
                                'finished, '
                                'rank, ' 
                                "DATE(finished, '-' || rank || ' DAYS') AS base_date "
                            'FROM '
                                'ranks'
                        ')'
                        'SELECT '
                            'user_id, '
                            'COUNT(*) AS streak, '
                            'MIN(finished) AS beginning, '
                            'MAX(finished) AS ending '
                        'FROM '
                            'groups '
                        'GROUP BY '
                            'user_id, base_date '
                        'HAVING '
                            'streak > 1 '
                        'ORDER BY '
                            'user_id, '
                            'finished;')
    print(f"Created /database/games{r}\n")

con.commit()
con.close()
