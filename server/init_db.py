import sys
import sqlite3
from os.path import exists


def myPrint(msg):
    try:
        app.logger.info(msg)
    except NameError:
        print(msg)

def initdb(file, overwrite=None):
    if not(exists(file)) or (overwrite != "overwrite"):
        if (overwrite == "overwrite"):
            myPrint("DB: Overwrite Database")
        else: 
            myPrint("DB: Creating Database")
        connection = sqlite3.connect(file)


        with open('./schema.sql') as f:
            connection.executescript(f.read())

        cur = connection.cursor()


        cur.execute("INSERT INTO users (username, passwd, email, name, room, status) VALUES (?, ?, ?, ?, ?, ?)",
                    ('luke', '1234', 'luke@desk.com', 'Luke Haliburton', '447', 1)
                    )

        cur.execute("INSERT INTO desks (macaddress, userid) VALUES (?, ?)",
                    ('00-14-22-04-25-37', cur.lastrowid)
                    )

        cur.execute("INSERT INTO users (username, passwd, email, name, room, status) VALUES (?, ?, ?, ?, ?, ?)",
                    ('robin', '1234', 'robin@desk.com',  'Robin Welsch', '447', 1)
                    )

        cur.execute("INSERT INTO desks (macaddress, userid) VALUES (?, ?)",
                    ('AA-14-22-04-25-37', cur.lastrowid)
                    )
        

        connection.commit()
        connection.close()

    else:
        myPrint("DB: Loading Existing Database")

if __name__ == "__main__":
    DATABASE_FILE = "database.db"

    print(sys.argv)
    if (len(sys.argv)>2):
        initdb(DATABASE_FILE, sys.argv[1])
    else:
        initdb(DATABASE_FILE)