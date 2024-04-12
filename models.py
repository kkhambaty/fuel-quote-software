from database import db
from sqlalchemy.orm import relationship 
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profiles = relationship('Profile', back_populates='user', lazy=True, cascade="all, delete, delete-orphan")
    fuel_quotes = relationship('FuelQuoteForm', back_populates='user', lazy=True, cascade="all, delete, delete-orphan")

class Profile(db.Model):
    __tablename__ = 'profile'
    UserID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
    FullName = db.Column(db.String(50), nullable=False)
    Address1 = db.Column(db.String(100), nullable=False)
    Address2 = db.Column(db.String(100))
    City = db.Column(db.String(100), nullable=False)
    State = db.Column(db.String(2), nullable=False)
    Zipcode = db.Column(db.String(9), nullable=False)
    user = relationship('User', back_populates='profiles')

class FuelQuoteForm(db.Model):
    __tablename__ = 'fuelquoteform'
    QuoteID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.ID'))
    GallonsRequested = db.Column(db.Numeric(10, 2), nullable=False)
    DeliveryAddress = db.Column(db.String(255))
    DeliveryDate = db.Column(db.Date, nullable=False)
    PricePerGallon = db.Column(db.Numeric(10, 2))
    TotalAmountDue = db.Column(db.Numeric(10, 2))
    user = relationship('User', back_populates='fuel_quotes')