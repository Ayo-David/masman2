from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.testdb#like the database

# connection = MongoClient('ds017584.mlab.com', 17584)
# db = connection['elearning']
# db.authenticate('elearning', 'elearning')

# MLAB = 'mongodb://elearning:elearning@ds017584.mlab.com:17584/elearning'
# client = MongoClient(MLAB, ConnectTimeoutMS=3000)
# db = client.elaern#like the database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register(report=None):
    if request.method=='POST':
        user = db.user
        existing_user = user.find_one({'name' : request.form['name']})
       
        if existing_user is None:
            
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            user.insert({'name':request.form['name'], 'password':hashpassword, 'email':request.form['email']})
            report =  'Successfully Register. You can now' + "<a href='/login'>Login</a>" 
        else:
            report = 'Already registered, please'  + "<a href='/login'>Login</a>"
    
    return render_template('register.html', report = report)


@app.route('/login', methods = ['POST', 'GET'])
def login(report=None):
    if request.method == 'POST':
        user = db.user
        login_user = user.find_one({'email' : request.form['email']})
       #myemail = login_user['email']
        #print (myemail)
        if login_user:
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'])
            #return hashpassword + login_user['password']
            if hashpassword == login_user['password']:
                session['email'] = request.form['email']
                
                #return login_user['password']                
            
                return redirect(url_for('courses'))
            #print (myemail)
            report =  'Invalid username/password'
    
    return render_template('login.html', report = report)


@app.route('/courses')
def courses():
    return render_template('landing.html', user=session['email'])
    

@app.route('/insert')
def start():
    user = db.user#a collection - like the table
    user.insert({'name' : 'Tayo', 'password':'ayodavid', 'email':'ayodavid@schoolshell.com'})
    user.insert({'name' : 'Promise', 'password':'sege', 'email':'sege@schoolshell.com'})
    user.insert({'name' : 'Akuna', 'password':'bayo'})
    return "It worked and inserted"

@app.route('/find')
def find():
    user = db.user
    myname = user.find_one({"name": "Tayo"})
    return 'my name is ' + myname["name"] + 'and my email is: ' + myname["email"]
    

if __name__ == "__main__":
    app.secret_key = '****mysecret////'
    app.run(debug = True)
    
    
