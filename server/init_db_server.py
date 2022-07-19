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
    
   
    cur.execute("INSERT INTO users (username, active, standkey, sitkey, cond) VALUES (%s, %s, %s, %s, %s)",
    ("luke", "1", "1", "2", "R"))
    userid = cur.lastrowid

    cur.execute("INSERT INTO desks (macaddress, location) VALUES (%s, %s)",
                ("10:27:f5:78:28:a4", "441 right")
                )

    cur.execute("INSERT INTO deskjoins (deskid, userid) VALUES (%s, %s)",
                (str(cur.lastrowid), str(userid))
                )
    connection.commit()
    connection.close()