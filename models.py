from datetime import datetime
import os

from sqlalchemy.orm import exc
from sqlalchemy.sql.functions import func
from settings import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, desc

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

    def json(self):
        return {'name': self.name}

    def get(_name):
        '''function to get movie using the id of the movie as parameter'''
        return Menu.query.filter_by(name=_name).first()


    def getAll():
        return [Menu.json(menu) for menu in Menu.query.filter(Dish.menuName == Menu.name).all()]

    def getAllOBName():
        return [Menu.json(menu) for menu in Menu.query.filter(Dish.menuName == Menu.name).order_by(Menu.name).all()]

    def getAllOBDish():
        return [Menu.json(menu) for menu in Menu.query.filter(Dish.menuName == Menu.name).group_by(Menu.name).order_by(desc(func.count(Dish.menuName))).all()]


    def add(_name):
        newMenu = Menu(name = _name)
        db.session.add(newMenu)
        try:
            db.session.commit()
        except exc.IntegrityError as ex:
            db.session.rollback()
            return ex
        return None

    def delete(self):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Menu.query.filter_by(name=self.name).delete()
        # filter movie by id and delete
        db.session.commit()  # commiting the new change to our database


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    menuName = db.Column(db.String(80), db.ForeignKey('menus.name'), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    timePreparation = db.Column(db.Integer, nullable=False)
    createdTime = db.Column(db.DateTime, default=datetime.utcnow)
    updatedTime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    vegan = db.Column(db.Boolean, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name,
                'menuName': self.menuName, 'description': self.description,
                'price': self.price, 'timePreparation': self.timePreparation,
                'createdTime': self.createdTime, 'updatedTime': self.updatedTime,
                'vegan': self.vegan}

    def get(_id):
        return Dish.query.filter_by(name=_id).first()

    def add(_name, _menuName, _description, _price, _timePreparation, _vegan):
        newDish = Dish(name = _name, menuName=_menuName, description = _description,
                       price = _price, timePreparation = _timePreparation,
                       vegan = _vegan)
        db.session.add(newDish)
        try:
            db.session.commit()
        except exc.IntegrityError as ex:
            db.session.rollback()
            return ex
        return None

    def update(_id, _name, _menuName, _description, _price, _timePreparation, _vegan):
        dish_to_update = Dish.query.filter_by(id=_id).first()

        dish_to_update.name = _name
        dish_to_update.menuName = _menuName
        dish_to_update.description = _description
        dish_to_update.price = _price
        dish_to_update.timePreparation = _timePreparation
        dish_to_update.vegan = _vegan
        try:
            db.session.commit()
        except exc.IntegrityError as ex:
            db.session.rollback()
            return ex
        return None

    def list(_menu, _substring):
        return [Dish.json(dish) for dish in Dish.query.filter(Dish.menuName==_menu, Dish.name.contains(_substring)).all()]
