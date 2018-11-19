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
            year=request.form['year']
            select_stm = "SELECT * FROM Games WHERE "
            data=[]
            if lgID!='':
                select_stm=select_stm + 'lgID=%s'
                data.append(lgID)
            if tmID:
                select_stm = select_stm + ' and tmID=%s'
                data.append(tmID)
            if year:
                select_stm = select_stm + ' and year=%s'
                data.append(year)
            debug=select_stm
            cur = mysql.connection.cursor()
            data = tuple(data)
            cur.execute(select_stm,data)
            rv = cur.fetchall()
            cur1 = mysql.connection.cursor()
            cur1.execute('''select distinct year from Games order by year''')
            years=cur1.fetchall()
            years=[items[0] for items in years]
            return render_template("teams.html", rv=rv, years=years, year=int(year), lgID=lgID, tmID=tmID)

        else:
            select_stm = "SELECT * FROM Games WHERE year =1972"
            cur = mysql.connection.cursor()
            cur.execute(select_stm)
            rv = cur.fetchall()
            cur1 = mysql.connection.cursor()
            cur1.execute('''select distinct year from Games order by year''')
            years=cur1.fetchall()
            years=[year[0] for year in years]
            return render_template("teams.html", rv=rv, years=years, year=1972, lgID='NHL', tmID='')    
    except Exception as e:
        debug=e
        return render_template("teams.html", debug=debug)
    



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
