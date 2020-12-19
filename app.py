

from flask import Flask, render_template, request, jsonify
import query_on_whoosh
import test_module
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