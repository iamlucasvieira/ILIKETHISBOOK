"""
Created on 23/08/2019

@author: Lucas V. dos Santos
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Signup(db.Model):
    __tablename__ = "signup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique= True)
    password = db.Column(db.String, nullable=False)

    # def newuser(self,name,email,password):

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    signup_id =db.Column(db.Integer, db.ForeignKey("signup.id"), nullable=False)