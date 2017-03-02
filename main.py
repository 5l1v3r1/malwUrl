import requests
import json
from flask import Flask,g,jsonify,request, Response,render_template
import sqlite3
from functools import wraps

app = Flask(__name__)

DATABASE = 'malwUrl.db'

COUNTER = 0

def check_auth(username, password):
	return username == 'frknozr' and password == 'password'

def authenticate():
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def index():
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute("select count(ip) from url")
	data = c.fetchall()
	return render_template("index.html",data = data[0][0])

@app.route("/api")
@requires_auth
def api():
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute("select ip from url")
	data = c.fetchall()
	ips = []
	for i in data:
		ips.append(i[0])
	conn.close()
	return jsonify({"ips":ips})

if __name__ == '__main__':
	app.run(debug=True)