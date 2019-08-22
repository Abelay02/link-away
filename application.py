from flask import Flask, render_template, redirect, request
from helpers import index2url, url2index
import psycopg2
import sqlalchemy as db
from psycopg2 import Error
app = Flask(__name__)

# @app.route('/', methods=["GET","POST"])
# def index():
#     return render_template('index.html')


engine = db.create_engine('postgresql+psycopg2://aabelay@localhost/url_db')
connection = engine.connect()
metadata = db.MetaData()


urls = db.Table('urls', metadata,
              db.Column('id', db.Integer(), primary_key=True),
              db.Column('long_url', db.String(255), nullable=False)
              )

metadata.create_all(engine) #Creates the table if not already existing



@app.route('/', methods=["GET", "POST"])
def shorten():
    """add url to db, return shortened URL"""

    # gives the user the form to request a stock quote
    if request.method == "GET":
        return render_template("index.html")

    else: 
        data = request.form.get("symbol")

        #### add data to DB
        query = db.insert(urls).values(long_url=data)
        ResultProxy = connection.execute(query)
        currid = ResultProxy.inserted_primary_key[0]

        ############################

        # return shortened url
        message = "localhost:5000/"+index2url(currid)
        return render_template("shortened.html",  message=message)





@app.route('/<name>')
def myfunc(name):
  ind = url2index(name)
  query = db.select([urls.columns.long_url]).where(urls.columns.id==ind)
  currid = connection.execute(query).scalar()
  return redirect('http://'+str(currid))








if __name__ == '__main__':
    app.run(debug=True)

