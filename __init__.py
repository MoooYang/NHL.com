from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = '47.107.75.241'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'WPI2018'
app.config['MYSQL_DB'] = 'HOCKEY'
mysql = MySQL(app)

def get_table(select_stm, data=None):
    cur = mysql.connection.cursor()
    if data==None:
        cur.execute(select_stm)
    else:
        data = tuple(data)
        cur.execute(select_stm,data)
    table = cur.fetchall()
    return table

def get_dropoff(select_stm):
    cur = mysql.connection.cursor()
    cur.execute(select_stm)
    results = cur.fetchall()
    drop=[items[0] for items in results]
    return drop

def rep_with_value(string, value):
    n = len(value)
    new_string = string
    for i in range(n):    
        rep = value[i]
        new_string = new_string.replace('%s',rep, 1)
    return new_string



@app.route("/")
def homepage():
    return render_template("homepage.html" )

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/teams/",methods=['POST','GET'])
def teams():
    try:
        if request.method=='POST':
            try:
                show= request.form['show']
            except:
                show = 'false'
            if show =='false':
                lgID=request.form['lgID']
                tmName1=request.form['tmName1']
                year=request.form['year1']
                ex1 =request.form['ex1']
                ex2 =request.form['ex2']
                ex3 =request.form['ex3']
                select_stm = "select name, year, lgId, tmID, rank, G, W, L, T ,Pts, GF, GA from Team where "
                where=''
                groupby=''
                data=[]
                if year:
                    where = where + 'and year=%s '
                    data.append(year)
                if lgID!='ALL':
                    where=where + 'and lgID=%s '
                    data.append(lgID)
                if tmName1:
                    where = where + 'and name like %s '
                    data.append('%'+ tmName1 +'%')
                if int(ex1):
                    where = where + 'and W >= %s '
                    data.append(ex1)
                if int(ex2):
                    where = where + 'and L >= %s '
                    data.append(ex2)
                if int(ex3):
                    where = where + 'and T >= %s '
                    data.append(ex3)
                title =['Team','Year','League','TeamID','Rank','Games','Wins','Losses','Ties','Pts','GF','GA']
            else:
                tmName=request.form['tmName']
                tmNameP=request.form['tmNameP']
                year=request.form['year2']
                select_stm = "select * from team_game where "
                where=''
                groupby=''
                data=[]
                if tmName:
                    where = where + 'and name like %s '
                    data.append('%'+tmName+'%')
                if tmNameP:
                    where = where + 'and pname like %s '
                    data.append('%'+tmNameP+'%')
                if year:
                    if year=='sum':
                        select_stm='select name, pname, sum(Wins), sum(Losses), sum(Ties) from team_game where '
                        groupby=' group by name, pname'
                        title = ['Home','Away','Wins','Losses','Ties']
                    else:
                        where = where + 'and year=%s '
                        data.append(year)
                        title = ['Year','Home','Away','Wins','Losses','Ties']
                else:
                    title = ['Year','Home','Away','Wins','Losses','Ties']
            where=where[3:]
            debug= select_stm+rep_with_value(where,data)+groupby
            table=get_table(select_stm+where+groupby, data)
            teamdrop=get_dropoff('select distinct name from Team')
            years=get_dropoff('select distinct year from Games order by year')
            try:
                year=int(year)
            except:
                year=''
            return render_template("teams.html", table=table, years=years, debug=debug, year=year,teamdrop=teamdrop,title=title)

        else:
            select_stm = "SELECT * FROM Games WHERE year =1927"
            table=get_table(select_stm)
            teamdrop=get_dropoff('select distinct name from Team')
            years=get_dropoff('select distinct year from Games order by year')
            return render_template("teams.html", table=table, years=years, year=1927, lgID='NHL', tmID='',teamdrop=teamdrop)    
    except Exception as e:
        debug=e
        return render_template("teams.html", debug=debug)
    



@app.route("/players/",methods=['POST','GET'])
def players():
    try:
        if request.method=='POST':
            lgID=request.form['lgID']
            tmID=request.form['tmID']
            year=request.form['year']
            pname=request.form['pname']
            postion=request.form['position']
            catch=request.form['catch']
            age=request.form['age']
            weight=request.form['weight']
            height=request.form['height']
            assists=request.form['assists']
            pts=request.form['pts']
            pim=request.form['pim']

            where=''
            select_stm = "SELECT * FROM player_team WHERE "
            data=[]
            if year:
                where = where + 'and Syear=%s '
                data.append(year)
            if lgID!='ALL':
                where=where + 'and lgID=%s '
                data.append(lgID)
            if tmID:
                where = where + 'and tname like %s '
                data.append('%'+tmID+'%')
            if int(weight)!=125:
                where = where + 'and weight >= %s '
                data.append(weight)
            if int(height)!=63:
                where = where + 'and height >= %s '
                data.append(height)
            if pname:
                where = where + 'and pname like %s '
                data.append('%'+pname+'%')
            if postion:
                where = where + 'and pos= %s '
                data.append(postion)
            if catch:
                where = where + 'and catch= %s '
                data.append(catch)
            if int(age)!=51:
                where = where + 'and AgebySeason <= %s '
                data.append(age)
            if int(assists):
                where = where + 'and Assists >= %s '
                data.append(assists)
            if int(pim):
                where = where + 'and PIM >= %s '
                data.append(pim)
            if int(pts):
                where = where + 'and Pts >= %s '
                data.append(pts)

        


            where=where[3:]
            debug=select_stm+rep_with_value(where,data)
            cur = mysql.connection.cursor()
            data = tuple(data)
            cur.execute(select_stm+where,data)
            table = cur.fetchall()
            cur1 = mysql.connection.cursor()
            cur1.execute('''select distinct year from Games order by year''')
            years=cur1.fetchall()
            years=[items[0] for items in years]
            pname_drop=get_dropoff('select distinct pname from player_team')
            teamdrop=get_dropoff('select distinct name from Team')
            try:
                year=int(year)
            except:
                year=''
            return render_template("players.html", debug=debug,table=table, years=years, year=year, lgID=lgID, tmID=tmID, pname_drop=pname_drop,teamdrop=teamdrop)

        else:
            select_stm = "SELECT * FROM player_team WHERE Syear =1927"
            cur = mysql.connection.cursor()
            cur.execute(select_stm)
            table = cur.fetchall()
            cur1 = mysql.connection.cursor()
            cur1.execute('''select distinct year from Games order by year''')
            years=cur1.fetchall()
            years=[year[0] for year in years]
            pname_drop=get_dropoff('select distinct pname from player_team')
            teamdrop=get_dropoff('select distinct name from Team')
            return render_template("players.html", table=table, years=years, year=1927, lgID='NHL', tmID='',pname_drop=pname_drop,teamdrop=teamdrop)    
    except Exception as e:
        debug=e
        return render_template("players.html", debug=debug)






@app.route("/coaches/")
def coaches():
    return render_template("coaches.html")
@app.route("/leaders/")
def leaders():
    return render_template("leaders.html")
   
if __name__ == "__main__":
    app.run()
