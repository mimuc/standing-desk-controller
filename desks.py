import sys,os  
sys.path.append(os.getcwd())

# import sqlite3
import json
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
import trigger_standing_all_modes
import mysql.connector

standing_threshold = 900
# DATABASE_FILE = "database.db"

config_file = open('secret.json')
config = json.load(config_file)


app = Flask(__name__)
app.config.from_mapping(config)

# Initialize the DB
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)
# cursor.execute("DROP TABLE IF EXISTS commands")
# cursor.execute("CREATE TABLE commands (commandid INT(11) PRIMARY KEY AUTO_INCREMENT, userid INT(11))") 
# conn.commit()
import init_db_server
init_db_server.initdb(conn)


# mysql.init_app(app)

# def trigger_standing():
#     trigger_standing_all_modes.run()
    


def get_db_connection():
    conn = mysql.connector.connect(**config)
    return conn

# def test_trigger():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     userid = 1
#     command = 1
#     cursor.execute('INSERT INTO commands (userid, command, done) VALUES(%s ,%s , %s)', (userid, command, 0 ))
#     conn.commit()
#     conn.close()
        


scheduler = APScheduler()
# scheduler.add_job(func=trigger_standing, trigger='cron', id='job1', minute=43, max_instances=1)
scheduler.init_app(app)
scheduler.start()



@scheduler.task("cron", id="job1", minute=50, max_instances=1)
def trigger_standing():
    trigger_standing_all_modes.run()

@app.route("/")
def index():
    return '''<h1 style='color:#00883A'>Welcome to LMU Standing Desks!</h1>
    <p>This project is created and operated by Luke Haliburton, Prof. Dr. Sven Mayer, and Prof. Dr. Albrecht Schmidt from LMU Munich</p>'''



@app.route('/users')
def allUsers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users") #userid, email
    rows = cursor.fetchall()

    
    conn.close()

    return  jsonify(rows)

@app.route('/users/add/<string:username>/<int:active>/<int:standkey>/<int:sitkey>/<string:condition>/<string:startdate>')
def addUser(username, active, standkey, sitkey, condition, startdate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO users (username, active, standkey, sitkey, cond, startdate) VALUES(%s, %s, %s, %s, %s, %s)', (username, active, standkey, sitkey, condition, startdate))
    conn.commit()
    conn.close()

    return  {"status":"added", "id":cursor.lastrowid}
   

@app.route('/users/condition/<string:condition>')
def usersByCondition(condition):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE cond = '{condition}'", ())
    rows = cursor.fetchall()
    
    conn.close()
    return jsonify(rows)


@app.route('/users/condition', methods=['GET'])
def usersByConditionGet():
    data = request.json   
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE cond = '{data['condition']}'", ())
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)
   
@app.route('/desks')
def allDesks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM desks")
    rows = cursor.fetchall()
    ret = []
    for row in rows:
        ret.append(str(row))
    conn.close()
    return  jsonify(rows)

@app.route('/desks/add/<string:macaddress>/<string:desklocation>')
def addDesk(macaddress, desklocation):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO desks (macaddress, desklocation) VALUES(%s, %s)', (macaddress, desklocation))
    conn.commit()
    conn.close()

    return  {"status":"added", "id":cursor.lastrowid}

@app.route('/heights')
def allHeights():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM heights")
    rows = cursor.fetchall()
    
    conn.close()
    return  jsonify(rows)
   

@app.route('/deskjoins')
def allDeskjoins():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM deskjoins")
    rows = cursor.fetchall()
    
    conn.close()
    return  jsonify(rows)
    

@app.route('/deskjoins/add/<string:username>/<string:desklocation>')
def addDeskjoin(username, desklocation):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'", ())
    rows1 = cursor.fetchall()
    
    if len(rows1) > 0:
        cur2 = conn.cursor(dictionary=True)
        cur2.execute(f"SELECT * FROM desks WHERE desklocation = '{desklocation}'", ())
        rows2 = cur2.fetchall()
        if len(rows2) > 0:
            cur3 = conn.cursor()
            cur3.execute("INSERT INTO deskjoins (userid, deskid) VALUES(%s, %s)", (rows1[0]['userid'], rows2[0]['deskid']))
            conn.commit()
            conn.close()
            return  {"status":"added", "id":cursor.lastrowid}
        else:
            conn.close()
            return {"status":"error", "reason": "could not find desk", "desklocation": desklocation}
    else:
        conn.close()
        return {"status":"error", "reason": "could not find user", "username": username}

@app.route('/commands')
def allCommands():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM commands")
    rows = cursor.fetchall()
    
    conn.close()
    return  jsonify(rows)
    


@app.route('/heights/id/<string:userid>')
def heightsById(userid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM heights WHERE userid = {userid}", ())
    rows = cursor.fetchall()
    
    conn.close()
    return  jsonify(rows)

@app.route('/heights/id', methods=['GET'])
def heightsByIdGet():
    data = request.json   
    conn = get_db_connection()
    if ('heighttime' in data):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM heights WHERE (userid = {data['userid']}) AND (created > '{data['heighttime']}')", ())
        rows = cursor.fetchall()
        conn.close()
    else:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM heights WHERE userid = {data['userid']}", ())
        rows = cursor.fetchall()
        conn.close()
    
    conn.close()
    return  jsonify(rows)


    
@app.route('/heights/u/<string:username>')
def heightsByUsername(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM heights JOIN users ON heights.userid = users.userid WHERE users.username = '{username}'")
    rows = cursor.fetchall()
    
    conn.close()
    return  jsonify(rows)


@app.route('/heights/add', methods=['POST']) 
def addHeightPost():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # We get the Macaddress of the desk - use this to look up the userid and then add the POSTed height to that userid
    cursor.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.enddate IS NULL)")
    rows = cursor.fetchall()
    
    if (len(rows) > 0):
        if ('heighttime' in data):
            cursor.execute("INSERT INTO heights (heighttime, userid, height) VALUES(%s,%s,%s)", (data['heighttime'], rows[0]['userid'], data['height']))
            conn.commit()
            conn.close()
            return  {"status":"added", "id": cursor.lastrowid}
        elif ('heighttimes' in data):
            lstIds=[]
            for i in range (len(data["heighttimes"])):
                cursor.execute("INSERT INTO heights (heighttime, userid, height) VALUES(%s, %s, %s)", (data['heighttimes'][i], rows[0]['userid'], data['heights'][i]))
                conn.commit()
                lstIds.append(cursor.lastrowid)
            conn.close()
            return  {"status":"added", "length": len(lstIds)}
    else:
        conn.close()
        return  {"status":"no desk", "macaddress": data['macaddress']}


@app.route('/heights/add/<string:macaddress>/<string:height>/<int:heighttime>')
def addHeight(macaddress, height, heighttime):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    rows = cursor.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{macaddress}') AND (deskjoins.enddate IS NULL)").fetchall()

    if (len(rows) == 1):
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO heights (heighttime, userid, height) VALUES(%s,%s,%s)', (heighttime, rows[0]["userid"], height))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cursor.lastrowid}
    else:
        conn.close()
        return  {"status":"error"}

@app.route('/commands/id', methods=['GET'])
def commandsByIdGet():
    data = request.json   
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM commands WHERE (userid = '{data['userid']}' AND done = 0)")
    newCommand = cursor.fetchall()
    if(len(newCommand) >= 1):
        cursor.execute(f"UPDATE commands SET done = 1 WHERE commandid = '{newCommand[0]['commandid']}'")
        conn.commit()
        conn.close()
        return  {"status": "success", "command": newCommand[0]['command']}
    else:
        conn.close()
        return {"status": "success", "command": None}
    
        
@app.route('/commands/mac', methods=['GET'])
def commandsByMacGet():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO accessLogger (macaddress) VALUES(%s)', (data['macaddress'],))
   
    # We get the Macaddress of the desk - use this to look up the userid and see if that userid has any commands
    cursor.execute(f"SELECT * FROM (deskjoins INNER JOIN users ON deskjoins.userid = users.userid) INNER JOIN desks ON deskjoins.deskid = desks.deskid WHERE (desks.macaddress = '{data['macaddress']}') AND (deskjoins.enddate IS NULL)")
    rows = cursor.fetchall()
    
    if (len(rows) == 1):
        cursor.execute(f"SELECT * FROM commands WHERE (userid = '{rows[0]['userid']}' AND done = 0)")
        newCommand = cursor.fetchall()
        if(len(newCommand) >= 1):
    
            cursor.execute(f"UPDATE commands SET done = 1 WHERE commandid = '{newCommand[0]['commandid']}'")
            conn.commit()
            conn.close()
            return  {"status": "success", "command": newCommand[0]['command']}
        else:
            conn.commit()
            conn.close()
            return {"status": "success", "command": None}
    else:
        conn.commit()
        conn.close()
        return  {"status":"error", "macaddress": data['macaddress']}


@app.route('/commands/id/<string:userid>')
def commandsById(userid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM commands WHERE (userid = {userid})",())
    rows = cursor.fetchall()
    
    conn.close()
    return  jsonify(rows)


@app.route('/commands/add/<string:userid>/<string:command>')
def addCommandById(userid, command):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE users.userid = '{userid}'")
    rows = cursor.fetchall()

    if (len(rows) == 1):
        cursor.execute('INSERT INTO commands (userid, command, done) VALUES(%s ,%s , %s)', (userid, command, 0 ))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cursor.lastrowid}
    else:
        conn.close()
        return  {"status":"error"}


@app.route('/commands/add/<string:username>/<string:command>')
def addCommandByUsername(username, command):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    rows = cursor.execute(f"SELECT * FROM users WHERE users.username = '{username}'").fetchall()

    if (len(rows) == 1):
        cursor.execute('INSERT INTO commands (userid, command, done) VALUES(%s ,%s , %s)', (rows[0]['userid'], command, 0 ))
        conn.commit()
        conn.close()
        return  {"status":"added", "id":cursor.lastrowid}
    else:
        conn.close()
        return  {"status":"error"}

@app.route('/commands/add', methods=['POST']) 
def addCommandPost():
    data = request.json
    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO commands (userid, command, done) VALUES(%s ,%s , %s)', (data['userid'], data['command'], 0))
    conn.commit()
    conn.close()
    return  {"status":"added", "id":cursor.lastrowid}

@app.route('/smart/add', methods=['POST']) 
def addSmartCommand():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(f"SELECT * FROM users WHERE username = '{data['username']}'")
    rows1 = cursor.fetchall()
    
    if len(rows1) > 0:
        cursor.execute(f"SELECT * FROM heights WHERE userid = '{rows1[0]['userid']}'")
        rows2 = cursor.fetchall()
        if len(rows2) > 0:
            if rows2[-1]['height'] > standing_threshold:
                print('user is already standing, no command')
                return {"status":"not added", "reason": "user already standing"}
            else:
                print('user is sitting, do command')
                cursor.execute('INSERT INTO commands (userid, command, done) VALUES(%s ,%s , %s)', (rows1[0]['userid'], rows1[0]['standkey'], 0))
                conn.commit()
                conn.close()
                return {"status":"added", "id":cursor.lastrowid}
        else:
            print('there are no heights, do command')
            cursor.execute('INSERT INTO commands (userid, command, done) VALUES(%s ,%s , %s)', (rows1[0]['userid'], rows1[0]['standkey'], 0))
            conn.commit()
            conn.close()
            return {"status":"added", "id":cursor.lastrowid}
    else:
        conn.close()
        return {"status":"error", "reason": "could not find user", "username": data['username']}

@app.route('/startupLogger/add', methods=['POST']) 
def addStartupLogPost():
    data = request.json
    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO startupLogger (macaddress, versionNumber) VALUES(%s ,%s)', (data['macaddress'], data['versionNumber']))
    conn.commit()
    conn.close()
    return  {"status":"added", "id":cursor.lastrowid}


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False, debug=False)