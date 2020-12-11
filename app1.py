
import query_on_whoosh
from flask import Flask, render_template, request, jsonify
import sqlite3

# turn this file (app.py) into a web app
app = Flask(__name__)
app.config.update(dict(JSONIFY_PRETTYPRINT_REGULAR=True))

# I want to build an app that has a route that listens to /
@app.route("/")
def handle_slash():
    requested_name = request.args.get("name")
    return render_template("index.html", user_name=requested_name)    



@app.route("/query", strict_slashes=False)
def handle_query():
    query_term = request.args.get("q")
    page_index = int(request.args.get("p"))
    return jsonify({"query_term": query_term, "search_results": query_on_whoosh.query(query_term, current_page=page_index)})

@app.route("/query_view", strict_slashes=False)
def handle_query_view():
    query_term = request.args.get("q")
    if not query_term:
        query_term = ""
    page_index = int(request.args.get("p"))
    if not page_index:
        page_index_arg = "1"

    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    #INSERT INTO search_terms(id, term, search_time)
    #VALUES(1, baby', strftime('%s', 'now));delete from search_terms; insert into search_terms (id,term,search_time) values (1, 'garbage, strftime('%s', 'now));
    #hacker line: BAD!!!
    #c.executescript("INSERT INTO search_terms (id, term, search_time) VALUES (1, '{query_term}', strftime('%s', 'now'));")
    c.execute("INSERT INTO search_terms (id, term, search_time) VALUES (?, ?, strftime('%s', 'now'));" {query_term})
    c.execute("SELECT * FROM search_terms;")
    rows = c.fetchall()
    conn.commit()
    conn.close()

    page_index = int(page_index_arg)
    search_results = query_on_whoosh.query(query_term, current_page=page_index)
    return render_template("query.html",
                            data = search_results[0]
                            query_term=query_term
                            page_cnt=math.ceil(search_results)
                            current_page=page_index
                            history_list=rows)

    @app.route("/about", strict_slashes=False)
    def handle_about():
        return render_template("about.html")

    @app.route("/success", strict_slashes=False)
    def handle_request():
        new_data = request.args.get("new_data")
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("scurran2@emich.edu", config.gmail_password)
        server.sendmail("scurran2@emich.edu","scurran2@emich.edu", message)
        return render_template("success.html", new_data = new_data)    