from flask import request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_principal import Permission, RoleNeed
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

from autoscaler import app

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Define User Role model
user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                      )


# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))


class Auth:

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['POST'])
    def login(self):
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username, password=password).first()

        if user is None:
            return jsonify({"error": "Invalid credentials"}), 401

        login_user(user)
        return jsonify({"message": "Login successful"}), 200

    scale_permission = Permission(RoleNeed('admin'))
