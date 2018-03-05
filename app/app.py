from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'elearn'
app.config['MONGO_URI'] = 'mongodb://elearn1:elearning@ds229415.mlab.com:29415/elearn'

mongo = PyMongo(app)

@app.route('/add')

@app.route('/')
def index():
    return "Hello World!"


def add():
    user = mongo.db
    user.insert({'name' : 'AyoDavid'})
    return 'Add user!'



#class Example(db.Document):
	#name = db.StringField()
    
#if __name__ == "__main__":
    #app.run()#