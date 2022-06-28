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
def allUsers():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM users').fetchall() #userid, email
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/users/condition/<string:condition>')
def usersByCondition(condition):
    conn = get_db_connection()
    
    rows = conn.execute(f"SELECT * FROM users WHERE condition = '{condition}'", ()).fetchall()
    return json.dumps( [dict(ix) for ix in rows] )


@app.route('/users/condition', methods=['GET'])
def usersByConditionGet():
    data = request.json   
    conn = get_db_connection()
    
    rows = conn.execute(f"SELECT * FROM users WHERE condition = '{data['condition']}'", ()).fetchall()
    return json.dumps( [dict(ix) for ix in rows] )
   
@app.route('/desks')
def allDesks():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM desks').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/heights')
def allHeights():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM heights').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/deskjoins')
def allDeskjoins():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM deskjoins').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/commands')
def allCommands():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM commands').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/heights/id/<string:userid>')
def heightsById(userid):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM heights WHERE userid = {userid}", ()).fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

    
@app.route('/heights/u/<string:username>')
def heightsByUsername(username):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM heights JOIN users ON heights.userid = users.userid WHERE users.username = '{username}'").fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/heights/add', methods=['POST']) 
def addHeightPost():
    data = request.json
    conn = get_db_connection()

    # We get the Macaddress of the desk - use this to look up the userid and then add the POSTed height to that userid
    rows = conn.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.end IS NULL)").fetchall()

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
        conn.close()
        return  {"status":"error", "macaddress": data['macaddress']}


@app.route('/heights/add/<string:macaddress>/<string:height>/<int:time>')
def addHeight(macaddress, height, time):
    conn = get_db_connection()

    rows = conn.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{macaddress}') AND (deskjoins.end IS NULL)").fetchall()

    if (len(rows) == 1):
        cur = conn.cursor()
        cur.execute('INSERT INTO heights (time, userid, height) VALUES(?,?,?)', (time, rows[0]["userid"], height))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cur.lastrowid}
    else:
        conn.close()
        return  {"status":"error"}

@app.route('/commands/id', methods=['GET'])
def commandsByIdGet():
    data = request.json   
    conn = get_db_connection()

    # We get the Macaddress of the desk - use this to look up the userid and see if that userid has any commands
    rows = conn.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.end IS NULL)").fetchall()
 
    if (len(rows) == 1):
        newCommand = conn.execute(f"SELECT * FROM commands WHERE (userid = '{rows[0]['userid']}' AND done = 0)").fetchall()
        if(len(newCommand) >= 1):
        
            cur = conn.cursor()
            cur.execute(f"UPDATE commands SET done = 1 WHERE commandid = '{newCommand[0]['commandid']}'")
            conn.commit()
           

            conn.close()
            return  {"status": "success", "command": newCommand[0]['command']}
        else:
            conn.close()
            return{"status": "success", "command": None}
    else:
        conn.close()
        return  {"status":"error", "macaddress": data['macaddress']}


@app.route('/commands/id/<string:userid>')
def commandsById(userid):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM commands WHERE (userid = {userid})",()).fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/commands/add/<string:userid>/<string:command>')
def addCommandById(userid, command):
    conn = get_db_connection()

    rows = conn.execute(f"SELECT * FROM users WHERE users.userid = '{userid}'").fetchall()

    if (len(rows) == 1):
        cur = conn.cursor()
        cur.execute('INSERT INTO commands (userid, command, done) VALUES(?,?,?)', (userid, command, 0 ))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cur.lastrowid}
    else:
        conn.close()
        return  {"status":"error"}


@app.route('/commands/add/<string:username>/<string:command>')
def addCommandByUsername(username, command):
    conn = get_db_connection()

    rows = conn.execute(f"SELECT * FROM users WHERE users.username = '{username}'").fetchall()

    if (len(rows) == 1):
        cur = conn.cursor()
        cur.execute('INSERT INTO commands (userid, command, done) VALUES(?,?,?)', (rows[0]['userid'], command, 0 ))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cur.lastrowid}
    else:
        conn.close()
        return  {"status":"error"}

@app.route('/commands/add', methods=['POST']) 
def addCommandPost():
    data = request.json
    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute('INSERT INTO commands (userid, command, done) VALUES(?,?,?)', (data['userid'], data['command'], 0))
    conn.commit()
    conn.close()
    return  {"status":"added", "id":cur.lastrowid}