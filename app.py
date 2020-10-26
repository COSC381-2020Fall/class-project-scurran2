from flask import Flask, render_template, request

# turn this file into a web app
app = Flask(__name__)

#flask route listens to / as path delimiter
@app.route("/")
def handle_slash():
    requested_name = request.args.get("name")
    #handle the request
    return render_template("index.html", name = requested_name)