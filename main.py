from flask import Flask,request
import sqlite3
from flask_restful import Api,Resource,reqparse,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Database_Creation(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    phone_number = db.Column(db.Integer,nullable=False)
    company_name = db.Column(db.String(100),nullable=False)

    # def __repr__(self):
    #     return f" User(name={name} , email={email} , phone = {phone_number})"

#db.create_all()
post_req = reqparse.RequestParser()
post_req.add_argument("name",type=str,help="Name of te user")
post_req.add_argument("email",type=str,help="Name of te user")
post_req.add_argument("password",type=str,help="Name of te user")
post_req.add_argument("phone_number",type=int,help="Name of te user")
post_req.add_argument("company_name",type=str,help="Name of te user")


get_req = reqparse.RequestParser()
get_req.add_argument("email",type=str,help="email of the user")
get_req.add_argument("password",type=str,help="email of the user")

resource_fields = {
    'id':fields.Integer,
    'name': fields.String,
    'phone_number':fields.Integer,
    'email':fields.String,
    'company_name':fields.String,
    'error':fields.String
}

conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute("Select max(id) from database__creation")
x = cur.fetchall()[0][0]
if x is None:
    ID = 1

else:
    ID = x+1

print("Maximum Number of IDs: ",ID-1)
class User_login_signup(Resource):
    @marshal_with(resource_fields)
    def get(self):
        email = get_req.parse_args()['email']
        password = get_req.parse_args()['password']
        result = Database_Creation.query.filter_by(email=email,password=password).first()
        if result is None or str(result)[-2] == "0":
            return {"error":"Invalid username or password"}
        else:
            return result

    @marshal_with(resource_fields)
    def post(self):
        global ID
        args = post_req.parse_args()
        result = Database_Creation.query.filter_by(email=args['email']).first()
        if result is not None:
            return {"error":"email already exist"}
        else:
            User = Database_Creation(id = ID,
                                     name=args['name'],
                                     email=args['email'],
                                     password=args['password'],
                                     phone_number=args['phone_number'],
                                     company_name=args['company_name'])

            ID += 1
            db.session.add(User)
            db.session.commit()
            return User,201

api.add_resource(User_login_signup,"/User/")

#api.add_resource(helloworld,"/Get/<string:name>")
if __name__ == "__main__":
    app.run(debug=True)