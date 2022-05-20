import sqlite3
import json
from flask import Flask, request

DATABASE_FILE = "database.db"

config = {
    "DEBUG": True,  # run app in debug mode
    "SECRET_KEY" : 'your secret key'
}


app = Flask(__name__)
app.config.from_mapping(config)


import init_db
init_db.initdb(DATABASE_FILE)

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return {"status":"running"}

@app.route('/users')
def allusers():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM users').fetchall() #userid, email
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/desks')
def alldesks():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM desks').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/heights')
def allheights():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM heights').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/deskjoins')
def alldeskjoins():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM deskjoins').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/heights/id/<string:userid>')
def heights(userid):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM heights WHERE userid = {userid}", ()).fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

    
@app.route('/heights/u/<string:username>')
def heightUser(username):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM heights JOIN users ON heights.userid = users.userid WHERE users.username = '{username}'").fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/heights/add', methods=['POST']) 
def addheightP():
    data = request.json
    conn = get_db_connection()

    rows = conn.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.end IS NULL)").fetchall()\

    if (len(rows) == 1):
        if ('time' in data):
            cur = conn.cursor()
            cur.execute('INSERT INTO heights (time, userid, height) VALUES(?,?,?)', (data['time'], rows[0]["userid"], data['height']))
            conn.commit()
            conn.close()
            return  {"status":"added", "id":cur.lastrowid}
        elif ('times' in data):
        
            cur = conn.cursor()
            lstIds=[]
            for i in range (len(data["times"])):
                
                cur.execute('INSERT INTO heights (time, userid, height) VALUES(?,?,?)', (data['times'][i], rows[0]["userid"], data['heights'][i]))
                conn.commit()
                lstIds.append(cur.lastrowid)
            conn.close()
            
            return  {"status":"added", "ids":lstIds}

    else:
        return  {"status":"error", "macaddress": data['macaddress']}


@app.route('/heights/add/<string:macaddress>/<string:height>/<int:time>')
def addheight(macaddress, height, time):
    conn = get_db_connection()

    rows = conn.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{macaddress}') AND (deskjoins.end IS NULL)").fetchall()

    if (len(rows) == 1):
        cur = conn.cursor()
        cur.execute('INSERT INTO heights (time, userid, height) VALUES(?,?,?)', (time, rows[0]["userid"], height))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cur.lastrowid}
    else:
        return  {"status":"error"}


#@app.route('/heights/add/<string:userid>/<string:height>/<int:time>')
#def addheight(userid, height, time):
#    conn = get_db_connection()
#    cur = conn.cursor()
#    cur.execute('INSERT INTO heights (userid, height, time) VALUES(?,?,?)', (userid, height, time))
#    conn.commit()
#    conn.close()
#    return  {"status":"added", "id":cur.lastrowid}