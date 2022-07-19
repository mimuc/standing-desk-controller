import mysql.connector


config = {
    "user": 'desks',
    "password": 'N.bc5.bCDK2R',
    "database": 'desks',
    "host": 'lmmihum-wsv03.srv.mwn.de',
    "port": '5000',
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()
conn.close()