from flask import render_template ,Flask ,request ,redirect ,session
import mysql.connector
import os
app=Flask(__name__)

app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="",database="user")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/Home')
def Home():
    if 'user_id' in session:
        return render_template('Home.html')
    else:
        return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `data` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
    .format(email,password))

    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/Home')
    else:
        return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `data` (`id`, `name`, `email`, `password`) VALUES (NULL, '{}', '{}', '{}');""".format(name,email,password))

    conn.commit()

    cursor.execute("""SELECT * FROM `data` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/Home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)