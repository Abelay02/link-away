from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from helpers import index2url, url2index
import psycopg2
import os
from psycopg2 import Error

from flask_heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/url_db'
heroku = Heroku(app)
db = SQLAlchemy(app)

# @app.route('/', methods=["GET","POST"])
# def index():
#     return render_template('index.html')


class URL(db.Model):
  __tablename__ = "urls"
  id = db.Column(db.Integer, primary_key=True)
  long_url = db.Column(db.String(255), nullable=False)

  def __init__(self,long_url):
    self.long_url = long_url


@app.route('/', methods=["GET", "POST"])
def shorten():
    """add url to db, return shortened URL"""

    # gives the user the form to request a stock quote
    if request.method == "GET":
        return render_template("index.html")

    else: 
        data = request.form.get("symbol")

        me = URL(data)

        #### add data to DB
        db.session.add(me)
        db.session.commit()
        currid = me.id

        ############################

        # return shortened url
        message = "localhost:5000/"+index2url(currid)
        return render_template("shortened.html",  message=message)





@app.route('/<name>')
def myfunc(name):
  ind = url2index(name)
  query = db.session.query(URL).filter(URL.id == ind)
  currid = query[0].long_url
  return redirect('http://'+str(currid))








if __name__ == '__main__':
    app.run(debug=True)
