from datetime import datetime
from sqlalchemy.orm import relationship
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:SQListhebest@localhost/firts_project'
app.config['SECRET_KEY'] = 'wet4yrther3hrthrl6reyh467hsyh07woret02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password,
        }

    def __repr__(self):
        return '<Article %r>' % self.id


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = relationship("Comments", back_populates="article")

    def __repr__(self):
        return '<Article %r>' % self.id


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = relationship("Article", back_populates="comments")

    def __repr__(self):
        return '<Article %r>' % self.id