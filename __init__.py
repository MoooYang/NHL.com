from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = '47.107.75.241'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'WPI2018'
app.config['MYSQL_DB'] = 'HOCKEY'
mysql = MySQL(app)

@app.route("/")
def homepage():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Games WHERE year = 1972''')
    rv = cur.fetchall()
    return render_template("dashboard.html" ,rv=rv)

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/teams/",methods=['POST','GET'])
def teams():
    try:
        if request.method=='POST':
            lgID=request.form['lgID']
            tmID=request.form['tmID']
            select_stm = "SELECT * FROM Games WHERE year =%s"
            data=[1972]
            if lgID:
                select_stm=select_stm + ' and lgID=%s'
                data.append(lgID)
            if tmID:
                select_stm = select_stm + ' and tmID=%s'
                data.append(tmID)
        else:
            select_stm = "SELECT * FROM Games WHERE year =%s"
            data=[1972]
        debug=select_stm
	cur = mysql.connection.cursor()
        data = tuple(data)
        cur.execute(select_stm,data)
        rv = cur.fetchall()
    except Exception as e:
        debug=e
	rv="fail"
    return render_template("teams.html", rv=rv, debug=debug)



@app.route("/players/")
def players():
    return render_template("players.html")
@app.route("/coaches/")
def coaches():
    return render_template("coaches.html")
@app.route("/leaders/")
def leaders():
    return render_template("leaders.html")
   
if __name__ == "__main__":
    app.run()
