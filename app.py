from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)
#MYSQL CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="mydb"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


#Loading Home Page
@app.route('/', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password)) 
        users = cursor.fetchone() 
        if users: 
            session['loggedin'] = True
            session['id'] = users['id'] 
            session['username'] = users['username'] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('home.html', msg = msg) 
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM employee"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)
    
#New User
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into employee(NAME,CITY,AGE) value (%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash('User Details Added')        
        return redirect(url_for("home"))
    return render_template("addUsers.html")
#update User
@app.route("/editUser/<string:id>",methods=['GET','POST'])

def editUser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update employee set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash('User Detail Updated')
        return redirect(url_for("home"))
        con=mysql.connection.cursor()
        
    sql="select * from employee where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUser.html",datas=res)
#Delete User
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from employee where ID=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted')
    return redirect(url_for("home"))

if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)






