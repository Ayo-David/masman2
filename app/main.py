from flask import Flask, render_template, request, session, redirect, url_for, g
from pymongo import MongoClient
import bcrypt
from flask_jsglue import JSGlue


app = Flask(__name__)
app.secret_key = '****mysecret////'
jsglue = JSGlue(app)

#app.config.from_object('config')

#client = MongoClient('localhost', 27017)
#db = client.testdb#like the database

# connection = MongoClient('ds017584.mlab.com', 17584)
# db = connection['elearning']
# db.authenticate('elearning', 'elearning')

#MLAB = 'mongodb://elearning:elearning@ds017584.mlab.com:17584/elearning'

MLAB = 'mongodb://mastros:mastros101@ds241578.mlab.com:41578/mastros'
client = MongoClient(MLAB, ConnectTimeoutMS=3000)
db = client.mastros#like the database

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST','GET'])
def register(report=None):
    if request.method =='POST':

        user = db.user
        generation1 = db.generation1
        generation2 = db.generation2
        generation3 = db.generation3


        existing_user = user.find_one({'username' : request.form['username']})

        referral_id = request.form['referral_id'].upper()

        #to check if the referral exist in the user database
        existing_referral = user.find_one({'referrer_id' : referral_id})

         #to fetch the refferal id from g1 as user_id
        referral_parent = referral_id[4:]

        rp = int(referral_parent)

        #to fetch a grand parent
        grand_parent = generation1.find_one({'user_id' : rp})

        grand_parent_refid = grand_parent['referral_id']

        grand_parent_refid =  grand_parent_refid[4:]

        gp = int(grand_parent_refid)

        #print (great grand_parent)
        gg_parent = generation1.find_one({'user_id' : gp})
        gps = gg_parent['referral_id']
       
        #report = 'Grand Parent' + grand_parent + 'Referal Parent' + str(referral_parent)
 
        #check if referral exist
        if existing_referral:

            user_id = user.find().count()+18
            referrer_id = 'MFNG'+ str(user_id)
            #referrer_id is the id the user can give to others to refer them to the platform
            #referral_id is the id of the person who refer you

            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())

            
            if existing_user is None:
            
            #user_id1 = user.find().sort([("_id", -1), ("user_id", -1)]).limit(1)
            #user_id += user_id1['user_id']
            #++user_id
            
            #hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                user.insert({
                    'user_id':user.find().count()+18, #auto increment in the db
                    'referrer_id':referrer_id,
                    'name':request.form['name'],
                    'username':request.form['username'], 
                    'password':hashpassword,
                    'email':request.form['email'],
                    'phone':request.form['phone'], 
                    'whatsapp_no':request.form['whatsapp_no'],
                    'address':request.form['address'], 
                    'nationality':request.form['nationality'], 
                    'next_of_kin':request.form['next_of_kin'], 
                    'next_phone':request.form['next_phone'],
                    'bank':request.form['bank'], 
                    'account_no':request.form['account_no'], 
                    'account_name':request.form['account_name'],
                    'marital_status':request.form['marital_status'],
                    'spouse_name':request.form['spouse_name'],
                    'date_of_marriage':request.form['date_of_marriage'],
                    'referral_name':request.form['referral_name'],
                    'referral_id':referral_id
                    })
                
                #if not within the 1st 12 (the first 12 will not have a referal) 
                if user_id>12:

                    generation1.insert({
                        'user_id':user_id, #auto increment in the db
                        'referral_id':referral_id #this is the parent of the user_id
                        })


                    if grand_parent:
                        generation2.insert({
                            'user_id':user_id, #auto increment in the db
                            'referral_id':referral_id,#this is the parent of the user
                            'grand_parent':grand_parent['referral_id'] #this is the grand-parent of the user
                            })

                        if gg_parent:
                            generation3.insert({
                                'user_id':user_id, #auto increment in the db
                                'referral_id':referral_id,
                                'grand_parent':grand_parent['referral_id'],
                                'gg_parent':gg_parent['referral_id']
                                })
                                

                report =  'Successfully Register. You can now Login'

            else:
                report = 'Username is not available, please try another username'
 
        else:
            #report = 'GG:'+ str(gps) + 'Grand Parent' + str(grand_parent_refid) + 'Referal Parent' + str(referral_parent)
            report = 'The referrer with REFERRAL ID:' + str(referral_id) + ', does not exist. Please confirm the ID with your referrer'

    return render_template('register.html', report = report)


@app.route('/login', methods = ['POST', 'GET'])
def login(report=None):
    if request.method == 'POST':
        session.pop('username', None)
        user = db.user
        login_user = user.find_one({'username' : request.form['username']})
       #myemail = login_user['email']
        #print (myemail)
        if login_user:
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'])
            #return hashpassword + login_user['password']
            if hashpassword == login_user['password']:
                session['username'] = request.form['username']
                
                #return login_user['password']                
            
                return redirect(url_for('userdashboard'))
            #print (myemail)
            report =  'Invalid username/password'
    
    return render_template('login.html', report = report)


@app.route('/logout')
def logout(report=None):
    session.pop('username', None)
    return redirect('http://www.mastros.com.ng')


@app.route('/userdashboard')
def userdashboard():
    #if session is set
    if g.user:                                                                                                                                                             
        user = db.user
        generation1 = db.generation1
        generation2 = db.generation2
        generation3 = db.generation3
        
        login_user = user.find_one({'username' : session['username']})
        myid = 'MFNG' + str(login_user['user_id'])
       
        #return render_template('userdashboard.html', user=session['email'])
        downline1 = user.find({'referral_id':myid})
        downline2 = generation2.find({'grand_parent':myid})
        downline3 = generation3.find({'gg_parent':myid})
        return render_template('referral.html', downline = downline1, downline2 = downline2, downline3 = downline3, user=session['username'], myid = myid)

    return render_template('login.html', report = report)   


@app.route('/courses')
def courses():
    return render_template('landing.html', user=session['email'])

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user= session['username']


@app.route('/logout')
def dropsession():
    session.pop('username', None)
    report = 'You are Successfully logged out'
    

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
    app.run(debug = True)
    
    
