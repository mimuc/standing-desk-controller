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


        cur.execute("INSERT INTO users (username, passwd, email, name, status) VALUES (?, ?, ?, ?, ?)",
                    ('luke', '1234', 'luke.haliburton@ifi.lmu.de', 'Luke Haliburton', 1)
                    )
        userid = cur.lastrowid

        cur.execute("INSERT INTO desks (macaddress, location) VALUES (?, ?)",
                    ('84:d8:1b:47:07:7e', '441 right')
                    )

        cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (?, ?)",
                    (cur.lastrowid, userid)
                    )

        cur.execute("INSERT INTO users (username, passwd, email, name, status) VALUES (?, ?, ?, ?, ?)",
                    ('robin', '1234', 'robin.welsch@ifi.lmu.de',  'Robin Welsch', 1)
                    )

        userid = cur.lastrowid

        cur.execute("INSERT INTO desks (macaddress, location) VALUES (?, ?)",
                    ('AA-14-22-04-25-37', '441 left')
                    )
                    
        cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (?, ?)",
                    (cur.lastrowid, userid)
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