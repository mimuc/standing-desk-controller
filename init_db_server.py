import sys
# import sqlite3
from os.path import exists


# def myPrint(msg):
#     try:
#         app.logger.info(msg)
#     except NameError:
#         print(msg)

def initdb(connection, overwrite=None):
    cur = connection.cursor()
    with open('./schema.sql') as f:
        
        sqlFile = f.read()
        f.close()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            if command.strip() != '':
                cur.execute(command)
    
    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("luke", "1", "1", "2", "R", "2022-07-10"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Apollo", "441right")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )

    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("JanLeusman", "1", "1", "2", "R", "2022-07-12"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Adonis", "441left")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )

    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("fakeuser1", "1", "1", "2", "R", "2022-07-20"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Hades", "fakeroom1")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )

    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("fakeuser2", "1", "1", "2", "R", "2022-07-20"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Achilles", "fakeroom2")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )
    
    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("fakeuser3", "1", "1", "2", "R", "2022-07-20"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Dionysus", "fakeroom3")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )
    
    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("fakeuser4", "1", "1", "2", "R", "2022-07-20"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Chronos", "fakeroom4")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )
    
    # User
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES (%s, %s, %s, %s, %s, %s)",
    ("fakeuser5", "1", "1", "2", "R", "2022-07-20"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, desklocation) VALUES (%s, %s)",
                ("Poseidon", "fakeroom5")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )
    
    connection.commit()
    connection.close()
           

        # cur = connection.cursor()


        
        

        # connection.commit()
       

    # else:
    #     print("DB: Loading Existing Database")

# if __name__ == "__main__":
#     DATABASE_FILE = "database.db"

#     print(sys.argv)
#     if (len(sys.argv)>2):
#         initdb(DATABASE_FILE, sys.argv[1])
#     else:
#         initdb(DATABASE_FILE)