from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:varun123@localhost:5432/postgres'

db = SQLAlchemy(app) 
api = Api(app)

class UserModel(db.Model): 
    print("User Model")

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self): 
        return f"User(name =` {self.name}, email = {self.email})"
    

class ThingModel(db.Model):
    __tablename__ = 'things'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))


user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all() 
        return users 
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])

        db.session.add(user) 
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user 
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

#THINGS TABLE
thing_args = reqparse.RequestParser()
thing_args.add_argument('name', type=str, required=True, help='Name is required')
thing_args.add_argument('owner_id', type=int, required=True, help='Owner ID is required')

thingsFields = {
    'id':fields.Integer,
    'name':fields.String,
    'owner_id':fields.Integer
}


class Things(Resource):
    @marshal_with(thingsFields)
    def get(self):
        things = ThingModel.query.all() 
        return things
    
    @marshal_with(thingsFields)
    def post(self):
        args = thing_args.parse_args()
        owner = UserModel.query.filter_by(id=args["owner_id"]).first()
        if not owner:
            abort(400, message="Invalid owner_id: User does not exist")
        thing = ThingModel(name=args["name"], owner_id=args["owner_id"])
        db.session.add(thing)
        db.session.commit()
        things = ThingModel.query.all()
        return things, 201
class Thing(Resource):
    @marshal_with(thingsFields)
    def get(self, id):
        thing = ThingModel.query.filter_by(id=id).first() 
        if not thing: 
            abort(404, message="Thing not found")
        return thing 
    
    @marshal_with(thingsFields)
    def patch(self, id):
        args = thing_args.parse_args()
        thing = ThingModel.query.filter_by(id=id).first()
        if not thing:
            abort(404, message="Thing not found")
        owner = UserModel.query.filter_by(id=args["owner_id"]).first()
        if not owner:
            abort(400, message="Invalid owner_id: User does not exist")
        thing.name = args["name"]
        thing.owner_id = args["owner_id"]
        db.session.commit()
        return thing
    
    @marshal_with(thingsFields)
    def delete(self, id):
        thing = ThingModel.query.filter_by(id=id).first() 
        if not thing: 
            abort(404, message="Thing not found")
        db.session.delete(thing)
        db.session.commit()
        things = ThingModel.query.all()
        return things


#--------
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

api.add_resource(Things, '/api/things/')
api.add_resource(Thing, '/api/things/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 