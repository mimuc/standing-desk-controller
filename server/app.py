import sqlite3
import json
from flask import Flask, request

DATABASE_FILE = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


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
    rows = conn.execute('SELECT userid, email FROM users').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/desks')
def alldesks():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM desks').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )

@app.route('/hights')
def allhights():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM hights').fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/hights/u/<string:userid>')
def hights(userid):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM hights WHERE userid = ?', (userid)).fetchall()
    conn.close()
    return  json.dumps( [dict(ix) for ix in rows] )


@app.route('/hights/add', methods=['POST']) 
def addhightP():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO hights (userid, hight) VALUES(?,?)', (data["userid"], data["hight"]))
    conn.commit()
    conn.close()
    return  {"status":"added", "id":cur.lastrowid}


@app.route('/hights/add/<string:userid>/<string:hight>')
def addhight(userid, hight):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO hights (userid, hight) VALUES(?,?)', (userid, hight))
    conn.commit()
    conn.close()
    return  {"status":"added", "id":cur.lastrowid}