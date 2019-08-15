from flask import Flask, render_template, redirect, request
from helpers import index2url, url2index
import psycopg2
from psycopg2 import Error
app = Flask(__name__)

# @app.route('/', methods=["GET","POST"])
# def index():
#     return render_template('index.html')



@app.route('/', methods=["GET", "POST"])
def shorten():
    """add url to db, return shortened URL"""

    # gives the user the form to request a stock quote
    if request.method == "GET":
        return render_template("index.html")

    else:	
        data = request.form.get("symbol")

        #### add data to DB
        connection = psycopg2.connect(user = "aabelay",
                                  password = "",
                                  host = "localhost",
                                  port = "5432",
                                  database = "url_db")
        cursor = connection.cursor()

        insert_value_query = '''INSERT INTO urls(long_url)
    	VALUES(%s) RETURNING id;'''

    	cursor.execute(insert_value_query,(data,))
    	currid = cursor.fetchone()
    	currid = currid[0]

    	connection.commit()

        if(connection):
            cursor.close()
            connection.close()
        ############################

        # return shortened url
        message = "localhost:5000/"+index2url(currid)
        return render_template("shortened.html",  message=message)





@app.route('/<name>')
def myfunc(name):
	ind = url2index(name)

	connection = psycopg2.connect(user = "aabelay",
                                  password = "",
                                  host = "localhost",
                                  port = "5432",
                                  database = "url_db")
	cursor = connection.cursor()

	select_value_query = '''SELECT * FROM urls WHERE
    	id = %s'''

    	cursor.execute(select_value_query, (ind,))
    	currid = cursor.fetchone()
    	currid = currid[1]
    	print(currid)

	return redirect('http://'+currid)








if __name__ == '__main__':
    app.run(debug=True)

