from flask import render_template
from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import request

app = Flask(__name__)
#modify theses to match the database you want to test
username = 'root'
password = 'password'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = 'localhost'
dbname   = '/testdb'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning
db = SQLAlchemy(app)

# Load the test.sql schema to your DB before testing
class User(db.Model):
    __tablename__ = 'users'
    ID = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))

    def __init__(self, first, last):
        self.fname = first
        self.lname = last

    def __repr__(self):
        return f"<first={self.fname}, last={self.lname}>"


@app.route("/")
def test():
    result = User.query.get(1)
    print(result)
    return render_template('test.html')
    
@app.route("/testsubmit", methods=['POST'])
def testsubmit():
    first = request.form.get("fname")
    last = request.form.get("lname")
    user = User(first, last)
    try:
        db.session.add(user)
        db.session.commit()

        result = User.query.all()
        for user in result:
            print(user)
        return jsonify(message='User added successfully'), 201
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return False