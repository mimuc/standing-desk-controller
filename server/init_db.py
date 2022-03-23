import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO desks (macaddress, user, name, room) VALUES (?, ?, ?, ?)",
            ('00-14-22-04-25-37', 'luke', 'Luke Haliburton', '447')
            )

cur.execute("INSERT INTO desks (macaddress, user, name, room) VALUES (?, ?, ?, ?)",
            ('AA-14-22-04-25-37', 'robin', 'Robin Welsch', '447')
            )

connection.commit()
connection.close()