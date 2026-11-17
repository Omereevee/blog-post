from main import app

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from flask import Flask, render_template,request
import smtplib

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)

class Blog(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    subtitle:Mapped[str] = mapped_column(String(250),nullable=False)
    author:Mapped[str] = mapped_column(String(250),nullable=False)
    image_url:Mapped[str] = mapped_column(String(250),nullable=False)
    body:Mapped[str] = mapped_column(String(250),nullable=False)
    date:Mapped[str] = mapped_column(String(250),nullable=False)

    def __repr__(self):
        return f'blog: {self.title}'

    with app.app_context():
        db.create_all()


