import sys,os  
sys.path.append(os.getcwd())

# import sqlite3
import json
from flask import Flask, render_template, request, jsonify
from flask_apscheduler import APScheduler
import trigger_standing_all_modes
import mysql.connector
from datetime import datetime

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

# ONLY EVER UNCOMMENT THIS IF YOU WANT TO RESET THE DATABASE!!
# import init_db_server
# init_db_server.initdb(conn)


# mysql.init_app(app)

def trigger_standing():
    trigger_standing_all_modes.run()
    


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
scheduler.add_job(func=trigger_standing, trigger='cron', id='job1', minute=50, max_instances=1)
scheduler.init_app(app)
scheduler.start()



# @scheduler.task("cron", id="job1", minute=50, max_instances=1)
# def trigger_standing():
#     trigger_standing_all_modes.run()

@app.route("/")
def index():
    return '''<h1 style='color:#00883A'>Welcome to LMU Standing Desks!</h1>
    <p>This project is created and operated by Luke Haliburton, Prof. Dr. Sven Mayer, and Prof. Dr. Albrecht Schmidt from LMU Munich</p>'''


@app.route("/status")
def status():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM desks")
    rows = cursor.fetchall()
   
    boards = []
    boots = []
    lasts = []
    actives = []
    for row in rows:
        boards.append(row['macaddress'])
        cursor.execute(f"SELECT * FROM startupLogger WHERE macaddress = '{row['macaddress']}' ORDER BY created DESC LIMIT 1", ())
        rows = cursor.fetchall()
        # boots.append(rows)
        if len(rows) > 0:
            for row in rows:
                boots.append(row['created'])
        else:
            boots.append('Not booted yet')
        
        cursor.execute(f"SELECT * FROM accessLogger WHERE macaddress = '{row['macaddress']}' ORDER BY created DESC LIMIT 1", ())
        rows = cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                lasts.append(row['created'])
                actives.append('Not Active' if (datetime.now() - row['created']).total_seconds() > 240 else 'Active'  )
        else:
            lasts.append('Not active yet')
            actives.append('Not active yet')


    return render_template('status.html', board1=boards[0], boot1=boots[0], last1=lasts[0], active1=actives[0],
    board2=boards[1], boot2=boots[1], last2=lasts[1],  active2=actives[1],
    board3=boards[2], boot3=boots[2], last3=lasts[2],  active3=actives[2],
    board4=boards[3], boot4=boots[3], last4=lasts[3],  active4=actives[3],
    board5=boards[4], boot5=boots[4], last5=lasts[4],  active5=actives[4],
    board6=boards[5], boot6=boots[5], last6=lasts[5],  active6=actives[5],
    board7=boards[6], boot7=boots[6], last7=lasts[6],  active7=actives[6],
    board8=boards[7], boot8=boots[7], last8=lasts[7],  active8=actives[7],
    board9=boards[8], boot9=boots[8], last9=lasts[8],  active9=actives[8],
    board10=boards[9], boot10=boots[9], last10=lasts[9],  active10=actives[9],
    board11=boards[10], boot11=boots[10], last11=lasts[10],  active11=actives[10],
    board12=boards[11], boot12=boots[11], last12=lasts[11],  active12=actives[11],
    board13=boards[12], boot13=boots[12], last13=lasts[12],  active13=actives[12],
    board14=boards[13], boot14=boots[13], last14=lasts[13],  active14=actives[13],
    board15=boards[14], boot15=boots[14], last15=lasts[14],  active15=actives[14],
    board16=boards[15], boot16=boots[15], last16=lasts[15],  active16=actives[15],
    board17=boards[16], boot17=boots[16], last17=lasts[16],  active17=actives[16],
    board18=boards[17], boot18=boots[17], last18=lasts[17],  active18=actives[17],
    board19=boards[18], boot19=boots[18], last19=lasts[18],  active19=actives[18],
    board20=boards[19], boot20=boots[19], last20=lasts[19],  active20=actives[19],
    board21=boards[20], boot21=boots[20], last21=lasts[20],  active21=actives[20])



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
    cursor.execute(f"SELECT * FROM users WHERE (cond = '{data['condition']}') AND (active = 1)", ())
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
    # if the request is time limited, only get recent heights
    if ('time' in data):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM heights WHERE (userid = {data['userid']}) AND (created > '{data['time']}')", ())
        rows = cursor.fetchall()

    # otherwise get them all
    else:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM heights WHERE userid = {data['userid']}", ())
        rows = cursor.fetchall()
        
    
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

@app.route('/startupLogger/macaddress', methods=['GET'])
def startupLogByMac():
    data = request.json   
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM startupLogger WHERE macaddress = '{data['macaddress']}' ORDER BY created DESC LIMIT 10", ())
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/accessLogger/macaddress', methods=['GET'])
def accessLogByMac():
    data = request.json   
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM accessLogger WHERE macaddress = '{data['macaddress']}' ORDER BY created DESC LIMIT 10", ())
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False, debug=False)