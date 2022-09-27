from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:SQListhebest@localhost/firts_project'
app.config['SECRET_KEY'] = 'wet4yrther3hrthrl6reyh467hsyh07woret02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


with app.app_context():
    from routes.route import *

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)