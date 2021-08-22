from datetime import datetime
import os

from sqlalchemy.orm import exc
from settings import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(80), primary_key=True)
    passHash = db.Column(db.String)

    def getUser(_name):
        '''function to get movie using the id of the movie as parameter'''
        return User.query.filter_by(name=_name).first()

    def add(_name, _password):
        newUser =User(name = _name,  passHash = generate_password_hash(_password))
        db.session.add(newUser)
        try:
            db.session.commit()
        except exc.IntegrityError as ex:
            db.session.rollback()
            return ex
        return None

    def checkPassword(self, _password):
        if check_password_hash(self.passHash, _password):
            return os.environ['TOKEN']
        else:
            return ''



class Menu(db.Model):
    __tablename__ = 'menus'
    name = db.Column(db.String(80), primary_key=True)
    dishes = db.relationship('Dish', cascade="all,delete", backref='menu', lazy=True)

    def add(_name):
        newMenu = Menu(name = _name)
        db.session.add(newMenu)
        try:
            db.session.commit()
        except exc.IntegrityError as ex:
            db.session.rollback()
            return ex
        return None


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    menuName = db.Column(db.String(80), db.ForeignKey('menus.name'), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    timePreparation = db.Column(db.Integer, nullable=False)
    createdTime = db.Column(db.DateTime, default=datetime.utcnow)
    updatedTime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    vegan = db.Column(db.Boolean, nullable=False)
