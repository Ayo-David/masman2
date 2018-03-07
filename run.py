from app.main import app 

if __name__ == '__main__':
    app.secret_key = '****mysecret////'
    app.run(debug = True)