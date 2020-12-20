

from flask import Flask, render_template, request, jsonify
import query_on_whoosh
import test_module
import smtplib
import config
import math
#import sqlite3


# turn this file (app.py) into a web app
app = Flask(__name__)
app.config.update(dict(JSONIFY_PRETTYPRINT_REGULAR=True))

# I want to build an app that has a route that listens to /
@app.route("/")
def handle_slash():
    requested_name = request.args.get("name")
    return render_template("index.html", user_name=requested_name)    

@app.route("/test")
def handle_test():
    input = "abc"
    return test_module.test(input)

@app.route("/query", strict_slashes = False)
def handle_query():
    query = request.args.get("q")
    page = int(request.args.get("p"))
    return jsonify({"query term": query, "page": page, "search results": query_on_whoosh.query(query, 10, page)})

@app.route("/query_view", strict_slashes = False)
def handle_query_view():
    query = request.args.get("q")
    if not query:
        query = ""

    page_arg = request.args.get("p")    
    if not page_arg:
            page = 1
    else: 
        page= int (page_arg)
   
    query_results = query_on_whoosh.query(query, 10, page)
    count_results = query_results[1]
    page_count = math.ceil(count_results/10)
    return render_template("query.html", 
                            results = query_results[0],
                            page_count = page_count,
                            query_term = query)

@app.route("/about", strict_slashes = False)
def handle_about():
    return render_template("about.html")   

@app.route("/success", strict_slashes = False)
def handle_request():
    new_data = request.args.get("new_data")
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("scurran2@emich.edu", config.gmail_password)
    message  = 'Subject: {}\n\n{}'.format("Request to add new data","request to add: " + new_data)
    server.sendmail("scurran2@emich.edu","scurran2@emich.edu",message )
    return render_template("success.html", new_data=new_data)    