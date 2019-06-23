from flask import Flask, render_template, request, session, redirect, url_for, g
from pymongo import MongoClient
import bcrypt
from flask_jsglue import JSGlue
from flask_mail import Mail, Message

from twilio.rest import Client

# from paystackapi.paystack import Paystack
# from paystackapi.transaction import Transaction
from python_paystack.paystack_config import PaystackConfig

#from python_paystack.objects.transactions import Transaction
#from python_paystack.managers import TransactionsManager


#from paystack.resource import TransactionResource

import random
import string


import datetime

now = datetime.datetime.now()
#from flask_pymongo import PyMongo


# paystack_secret_key = "5om3secretK3y"  
# paystack = Paystack(secret_key=paystack_secret_key)


PaystackConfig.SECRET_KEY  = 'sk_test_54c9087ce1469555cd74a049d27b2b8e1cbc680e'
PaystackConfig.PUBLIC_KEY = "pk_test_9137b970012f0c420753ef1248d777f397282e12"



app = Flask(__name__)
app.secret_key = '****mysecret////'
jsglue = JSGlue(app)


#app.config.from_pyfile('config.cfg')

#mail = Mail(app)

###


###

#client = MongoClient('localhost', 27017)
#db = client.testdb#like the database



#client = Client("AC2b4ce9218ea8c9e87d694afa440acce2", "d76cd7ef786934e85502d19959c73f73")


MLAB = 'mongodb://mastros:mastros101@ds241578.mlab.com:41578/mastros'
#client = MongoClient(MLAB, ConnectTimeoutMS=3000)
#db = client.mastros#like the database

#mongo = PyMongo(app)
#db = mongo.mastros

client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.mastros    #Select the database
#todos = db.todo #Select the collection


twilioclient = Client("AC2b4ce9218ea8c9e87d694afa440acce2", "d76cd7ef786934e85502d19959c73f73")#for SMS


#client_sms = nexmo.Client(key='990ff089', secret='DR3yP8LVAKpsMow4')

@app.route('/')
def index():
    return render_template('register.html')



@app.route('/register', methods=['POST','GET'])
def register(report=None):
    report = ''
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



    
        #report = 'Grand Parent' + grand_parent + 'Referal Parent' + str(referral_parent)
 
        #check if referral exist
        if existing_referral:
            #assign id to the new user
            user_id = user.find().count()+1
            referrer_id = 'MFNG'+ str(user_id)

            if user_id>1:

                #to fetch a grand parent
                grand_parent = generation1.find_one({'user_id' : rp})

                grand_parent_refid = grand_parent['referral_id']

                grand_parent_refid =  grand_parent_refid[4:]

                gp = int(grand_parent_refid)

                #print (great grand_parent)
                gg_parent = generation1.find_one({'user_id' : gp})
                gps = gg_parent['referral_id']

            #referrer_id is the id the user can give to others to refer them to the platform
            #referralid is the id of the person who refer you

            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        #user_id = 1
        #referrer_id = 'MFNG'+ str(user_id)

            
            if existing_user is None:
            
            #user_id1 = user.find().sort([("_id", -1), ("user_id", -1)]).limit(1)
            #user_id += user_id1['user_id']
            #++user_id
              
                hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                
                user.insert({
                    'user_id':user.find().count()+1, #auto increment in the db #'user_id':1,
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
                #to reward referral if he has 6 downline
                reward(referral_id)
                
                #if not within the 1st 12 (the first 12 will not have a referal) 
                #anytime a new user register, g1, g2, g3 is updated for the referral and the user who has those parents
                #from g1, g2, g3 get all the downline t a user
                if user_id<1:

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

                    
                          
                    message = 'Congratulations! Thank you for signing up for MASTROS. Your unique ID to refer others is: MFNG' + str(user_id) + '. MASTROS, Creating uncommon millionaires from common people.'
                    
                    phone_no = '+234' + request.form['phone'] 
                    #response = client_sms.send_message({
                    
                    twilioclient.messages.create(to=phone_no, from_='MASTROS', body = message)
                    # response_txt = response['status'][0]
                    # if response['status'] == '0':
                    #     return 'Sent message ' + response['message-id'] + request.form['phone']
                    # else:
                    #     return 'Error: ' + response['error-text'] + request.form['phone']
                    

                report =  'Congratulations! To Complete your registration, please click on the payment link below'

                return render_template('success.html', report = report)

                #else:
                   # report = 'Username is not available, please try another username'
     
        else:
            #report = 'GG:'+ str(gps) + 'Grand Parent' + str(grand_parent_refid) + 'Referal Parent' + str(referral_parent)
            report = 'The referrer with REFERRAL ID:' + str(referral_id) + ', does not exist. Please confirm the ID with your referrer'
            #report = 'The referrer with REFERRAL ID does not exist. Please confirm the ID with your referrer'

    return render_template('register.html', report = report)




@app.route('/register_admin', methods=['POST','GET'])
def register_admin(report=None):

    report = ''
    if request.method =='POST':

        admin = db.admin

        existing_admin = admin.find_one({'username' : request.form['username']})
        
    
        #report = 'Grand Parent' + grand_parent + 'Referal Parent' + str(referral_parent)
 
           
            
        if existing_admin is None:
                
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                
            admin.insert({
                'admin_id':admin.find().count()+1, #auto increment in the db #'user_id':1,
                'name':request.form['name'],
                'username':request.form['username'], 
                'password':hashpassword,
                'email':request.form['email'],
                'phone':request.form['phone']
                })
                
                
                    

            report =  'Successful! You have been Successfully registered as an administrator'

            return render_template('success_admin.html', report = report)
     
        else:
            
            report = 'The admin already exist. Please register a new administrator'
            
    return render_template('register_admin.html', report = report)




def reward(myid):
    user = db.user
    generation1 = db.generation1
    generation2 = db.generation2
    generation3 = db.generation3
    myStatus = db.status
    
    #login_user = user.find_one({'username' : session['username']})
    #myid = 'MFNG' + str(login_user['user_id'])
   
    downline1_count = user.find({'referral_id':myid}).count()
    downline2_count = generation2.find({'grand_parent':myid}).count()
    downline3_count = generation3.find({'gg_parent':myid}).count()

    if downline1_count > 6:
        myStatus.insert({
            'date': now.strftime("%Y-%m-%d %H:%M"),
            'user_id': myid,
            'status': "Sales Rep",
            'reward': 'N11,380'
        })
    elif downline2_count == 36:
        myStatus.insert({
            'date': now.strftime("%Y-%m-%d %H:%M"),
            'user_id': myid,
            'status': "Supervisor 1",
            'reward': 'N30,000'
        })
    elif downline3_count == 72:
        myStatus.insert({
            'date': now.strftime("%Y-%m-%d %H:%M"),
            'user_id': myid,
            'status': "Supervisor 2",
            'reward': 'N90,000'
        })

@app.route('/myreward')
def myreward(report=None):
    if g.user:                                                                                                                                                             
        user = db.user
        
        myStatus = db.status
        
        login_user = user.find_one({'username' : session['username']})
        myid = 'MFNG' + str(login_user['user_id'])

        status = myStatus.find({'user_id':myid})
    
        return render_template('myreward.html', mystatus = status, user=session['username'], myid = myid,)

    return render_template('login.html', report = report) 


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
            #if hashpassword == login_user['password']:
            session['username'] = request.form['username']
                
                #return login_user['password']                
            
            return redirect(url_for('userdashboard'))
            #print (myemail)
            report =  'Invalid username/password'
    
    return render_template('login.html', report = report)


@app.route('/payment', methods = ['POST', 'GET'])
def payment():
        rand = ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in range(16)])
        secret_key = 'k_test_54c9087ce1469555cd74a049d27b2b8e1cbc680e'
        random_ref = rand
        test_email = 'ayodavid.ajayi@gmail.com'
        test_amount = '200000'
        plan = 'Basic'
        ref = '1234567890'
        client = TransactionResource(secret_key, random_ref)
        response = client.initialize(test_amount,test_email,plan)
        print(response)
        client.authorize() # Will open a browser window for client to enter card details
        verify = client.verify() # Verify client credentials
        print(verify)
        print(client.charge()) # Charge an already exsiting client


    # transaction = Transaction(2000, 'email@test.com')
    # transaction_manager = TransactionsManager()
    # transaction = transaction_manager.initialize_transaction('STANDARD', transaction)
    #Starts a standard transaction and returns a transaction object

    # transaction.authorization_url
    #Gives the authorization_url for the transaction

    #Transactions can easily be verified like so
    # transaction = transaction_manager.verify_transaction(transaction)



    # response = Transaction.initialize(reference='reference', amount='amount', email='email')
    # response = Transaction.charge(reference='reference', authorization_code='authorization_code',email='email', amount='amount')
    # return render_template('makePayment.html')    

    # -----------------





@app.route('/admin', methods = ['POST', 'GET'])
def admin(report=None):
    if request.method == 'POST':
        session.pop('username', None)
        admin = db.admin
        login_user = admin.find_one({'username' : request.form['username']})
       #myemail = login_user['email']
        #print (myemail)
        if login_user:
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'])
            #return hashpassword + login_user['password']
            #if hashpassword == login_user['password']:
            session['admin'] = request.form['username']
            g.user = session['admin']
                
                #return login_user['password']                
            
            return redirect(url_for('admindashboard'))
            #print (myemail)
            report =  'Invalid username/password'
    
    return render_template('admin_login.html', report = report)


@app.route('/logout')
def logout(report=None):
    session.pop('username', None)

    # msg = Message('HELLO', sender = 'ayodavid.ajayi@gmail.com', recipients = ['ayodavid@schoolshell.com'])
    # mail.send(msg)
    # return "Mesage sent"

    return redirect('http://www.mastros.com.ng')

@app.route('/adminlogout')
def adminlogout(report=None):
    session.pop('admin', None)

    # msg = Message('HELLO', sender = 'ayodavid.ajayi@gmail.com', recipients = ['ayodavid@schoolshell.com'])
    # mail.send(msg)
    # return "Mesage sent"

    return redirect('http://www.mastros.com.ng')


@app.route('/userdashboard')
def userdashboard():
    #if session is set
    if g.user:                                                                                                                                                             
        user = db.user
        generation1 = db.generation1
        generation2 = db.generation2
        generation3 = db.generation3
        myStatus = db.status
        
        login_user = user.find_one({'username' : session['username']})
        myid = 'MFNG' + str(login_user['user_id'])

        status = myStatus.find({'user_id':myid}).limit(1).sort('date',-1)
        #status = myStatus.find({'user_id':myid}).limit(1)
        

       
        #return render_template('userdashboard.html', user=session['email'])
        downline1 = user.find({'referral_id':myid})
        
        downline2 = generation2.find({'grand_parent':myid})
        downline3 = generation3.find({'gg_parent':myid})

        #leftjoin here

        #return status['status']
        return render_template('referral.html', downline = downline1, downline2 = downline2, downline3 = downline3, user=session['username'], myid = myid, mystatus = status)

    return render_template('login.html', report = report)   


@app.route('/admindashboard')
def admindashboard():
    #if session is set
    report =''
    if session['admin']:  
        admin = db.admin                                                                                                                                                           
        user = db.user
        generation1 = db.generation1
        generation2 = db.generation2
        generation3 = db.generation3
        myStatus = db.status
        
        login_admin = admin.find_one({'username' : session['admin']})
        myid = 'MFNG' + str(login_admin['admin_id'])

        #status = myStatus.find({'user_id':myid}).limit(1).sort('date',-1)

       
        #return render_template('userdashboard.html', user=session['email'])
        registerusers = user.find()
        
        #return status['status']
        return render_template('admin.html', registerusers = registerusers, admin=session['admin'], myid = myid)

    return render_template('admin_login.html', report = report)   


@app.route('/courses')
def courses():
    return render_template('landing.html', user=session['email'])

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


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
    myname = user.find_one({"name": "ayodavid"})
    return 'my name is ' + myname["name"] + 'and my email is: ' + myname["email"]
    

if __name__ == "__main__":
    app.run(debug = True)
    
    
