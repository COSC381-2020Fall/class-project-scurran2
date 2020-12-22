

from flask import Flask, render_template, request, jsonify
import query_on_whoosh
import test_module
import smtplib
import config
import math
import sqlite3


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
         
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    #SQlite injection
    #baby', strftime('%s','now')); delete from search_terms; insert into search_terms (id, term, search_time) values (1, 'never_gonna_give_you_up
    #c.executescript(f"INSERT INTO search_terms (id, term, search_time) VALUES (1, '{query}', strftime('%s','now'));");
    
    c.execute("SELECT enabled FROM settings WHERE feature='history';")
    history = c.fetchall()
    history_on = bool(history[0][0])
    if query != "" and history_on:
        c.execute("INSERT INTO search_terms (topic, term, search_time) VALUES ('Montessori', ?, strftime('%s','now'));", (query,))
    c.execute("SELECT * FROM search_terms;")
    conn.commit()
    conn.close()
    query_results = query_on_whoosh.query(query, 10, page)
    count_results = query_results[1]
    page_count = math.ceil(count_results/10)
    return render_template("query.html", 
                            results = query_results[0],
                            page_count = page_count,
                            query_term = query,
                            history_on = history_on)

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

@app.route("/history", strict_slashes=False)
def handle_history():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT topic, term, strftime('%m/%d/%Y %H:%M', search_time,'unixepoch','-5 hours') FROM search_terms;")
    rows = c.fetchall()
    c.execute("SELECT id FROM search_terms")
    names = c.fetchall()
    ids = []
    for item in names:
        for i in item:
            ids.append(i)
    conn.commit()
    conn.close()
    return render_template("history.html", history_list = rows, ids=ids)

@app.route("/remove_history", strict_slashes=False)
def handle_remove():
    id = request.args.get("id")
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    command = "DELETE FROM search_terms Where id = "+id
    c.execute(command)
    conn.commit()
    conn.close()
    return render_template("remove_history.html", id = id)

@app.route("/settings", strict_slashes=False)
def handle_settings():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT enabled FROM settings WHERE feature='history';")
    history = c.fetchall()
    history_on = bool(history[0][0])
    conn.commit()
    conn.close()
    return render_template("settings.html",history_on=history_on)

@app.route("/save_settings", strict_slashes=False)
def handle_save():
    enabled = request.args.get("enabled")
    command = "UPDATE settings SET enabled="
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    if enabled:
        c.execute(command + '1')
    else:
        c.execute(command + '0')  
    conn.commit()
    conn.close()
    return render_template("save_settings.html", enabled=enabled)    