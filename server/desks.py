import sys,os  
sys.path.append(os.getcwd())

# import sqlite3
import json
from flask import Flask, request
from flask_apscheduler import APScheduler
import trigger_standing_all_modes
import mysql.connector

standing_threshold = 900
# DATABASE_FILE = "database.db"


config = {
    "user": 'desks',
    "password": 'N.bc5.bCDK2R',
    "database": 'desks',
    "host": 'localhost',
    "port": '3306',
}




app = Flask(__name__)
app.config.from_mapping(config)

# Initialize the DB
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS commands")
# cursor.execute("CREATE TABLE commands (commandid INT(11) PRIMARY KEY AUTO_INCREMENT, userid INT(11))") 
# conn.commit()
import init_db_server
init_db_server.initdb(conn)


# mysql.init_app(app)

def trigger_standing():
    with app.app_context():
        print('running all conditions')
        trigger_standing_all_modes.run()


scheduler = APScheduler()
scheduler.add_job(func=trigger_standing, trigger='cron', id='job1', minute=22)
scheduler.start()

def get_db_connection():
    conn = mysql.connector.connect(**config)
    return conn


@app.route("/")
def index():
    return '''<h1 style='color:#00883A'>Welcome to LMU Standing Desks!</h1>
    <p>This project is created and operated by Luke Haliburton, Prof. Dr. Sven Mayer, and Prof. Dr. Albrecht Schmidt from LMU Munich</p>'''



@app.route('/users')
def allUsers():
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM `users`") #userid, email
        # rows = cur.fetchall()
        conn.close()

        return  json.dumps( [row for row in cur] )
        
        # return {"Something went right": cursor}
    except mysql.connector.Error as err:
        return {"Something went wrong": err}

@app.route('/users/add/<string:username>/<string:passwd>/<string:email>/<string:name>/<int:active>/<int:standkey>/<int:sitkey>/<string:condition>/<string:startdate>')
def addUser(username, passwd, email, name, active, standkey, sitkey, condition, startdate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, passwd, email, name, active, standkey, sitkey, cond, startdate) VALUES(?,?,?,?,?,?,?,?,?)', (username, passwd, email, name, active, standkey, sitkey, condition, startdate))
    conn.commit()
    conn.close()

    return  {"status":"added", "id":cur.lastrowid}
   

@app.route('/users/condition/<string:condition>')
def usersByCondition(condition):
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM users WHERE cond = '{condition}'", ()).fetchall()
    return json.dumps( [dict(ix) for ix in rows] )


@app.route('/users/condition', methods=['GET'])
def usersByConditionGet():
    data = request.json   
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM users WHERE cond = '{data['condition']}'", ()).fetchall()
    conn.close()
    return json.dumps( [dict(ix) for ix in rows] )
   
@app.route('/desks')
def allDesks():
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute('SELECT * FROM desks').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/desks/add/<string:macaddress>/<string:location>')
def addDesk(macaddress, location):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO desks (macaddress, location) VALUES(?,?)', (macaddress, location))
    conn.commit()
    conn.close()

    return  {"status":"added", "id":cur.lastrowid}

@app.route('/heights')
def allHeights():
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute('SELECT * FROM heights').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/deskjoins')
def allDeskjoins():
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute('SELECT * FROM deskjoins').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/deskjoins/add/<string:username>/<string:location>')
def addDeskjoin(username, location):
    conn = get_db_connection()
    cur = conn.cursor()
    rows1 = cur.execute(f"SELECT * FROM users WHERE username = '{username}'", ()).fetchall()
    print(rows1)
    if len(rows1) > 0:
        cur = conn.cursor()
        rows2 = cur.execute(f"SELECT * FROM desks WHERE location = '{location}'", ()).fetchall()
        if len(rows2) > 0:
            cur = conn.cursor()
            cur.execute('INSERT INTO deskjoins (userid, deskid) VALUES(?,?)', (rows1[0]['userid'], rows2[0]['deskid']))
            conn.commit()
            conn.close()
            return  {"status":"added", "id":cur.lastrowid}
        else:
            conn.close()
            return {"status":"error", "reason": "could not find desk", "location": location}
    else:
        conn.close()
        return {"status":"error", "reason": "could not find user", "username": username}

@app.route('/commands')
def allCommands():
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute('SELECT * FROM commands').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/heights/id/<string:userid>')
def heightsById(userid):
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM heights WHERE userid = {userid}", ()).fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/heights/id', methods=['GET'])
def heightsByIdGet():
    data = request.json   
    conn = get_db_connection()
    if ('time' in data):
        cur = conn.cursor()
        rows = cur.execute(f"SELECT * FROM heights WHERE (userid = {data['userid']}) AND (created > '{data['time']}')", ()).fetchall()
        conn.close()
    else:
        cur = conn.cursor()
        rows = cur.execute(f"SELECT * FROM heights WHERE userid = {data['userid']}", ()).fetchall()
        conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


    
@app.route('/heights/u/<string:username>')
def heightsByUsername(username):
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM heights JOIN users ON heights.userid = users.userid WHERE users.username = '{username}'").fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/heights/add', methods=['POST']) 
def addHeightPost():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    # We get the Macaddress of the desk - use this to look up the userid and then add the POSTed height to that userid
    rows = cur.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.end IS NULL)").fetchall()

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
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{macaddress}') AND (deskjoins.end IS NULL)").fetchall()

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
    cur = conn.cursor()
    # We get the Macaddress of the desk - use this to look up the userid and see if that userid has any commands
    rows = cur.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.end IS NULL)").fetchall()

    if (len(rows) == 1):
        cur = conn.cursor()
        newCommand = cur.execute(f"SELECT * FROM commands WHERE (userid = '{rows[0]['userid']}' AND done = 0)").fetchall()
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
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM commands WHERE (userid = {userid})",()).fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/commands/add/<string:userid>/<string:command>')
def addCommandById(userid, command):
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM users WHERE users.userid = '{userid}'").fetchall()

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
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM users WHERE users.username = '{username}'").fetchall()

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

@app.route('/smart/add', methods=['POST']) 
def addSmartCommand():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    rows1 = cur.execute(f"SELECT * FROM users WHERE username = '{data['username']}'").fetchall()
    if len(rows1) > 0:
        cur = conn.cursor()
        rows2 = cur.execute(f"SELECT * FROM heights WHERE userid = '{rows1[0]['userid']}'").fetchall()
        if len(rows2) > 0:
            print('there are heights')
            print(rows2[-1]['height'])
            if rows2[-1]['height'] > standing_threshold:
                print('user is already standing, no command')
                return {"status":"not added", "reason": "user already standing"}
            else:
                print('user is sitting, do command')
                cur = conn.cursor()
                cur.execute('INSERT INTO commands (userid, command, done) VALUES(?,?,?)', (rows1[0]['userid'], rows1[0]['standkey'], 0))
                conn.commit()
                conn.close()
                return {"status":"added", "id":cur.lastrowid}
        else:
            print('there are no heights, do command')
            cur = conn.cursor()
            cur.execute('INSERT INTO commands (userid, command, done) VALUES(?,?,?)', (rows1[0]['userid'], rows1[0]['standkey'], 0))
            conn.commit()
            conn.close()
            return {"status":"added", "id":cur.lastrowid}
    else:
        conn.close()
        return {"status":"error", "reason": "could not find user", "username": data['username']}



if __name__ == "__main__":
    app.run(host='0.0.0.0')