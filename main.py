from flask import Flask, render_template
from math_help import math_help

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(math_help)

# Home page
@app.route("/")
@app.route("/index")
def index_test():
  return render_template("index.html")

@app.route("/vaccines")
def vaccines_route():
  return render_template("vaccines.html")

app.run(host='0.0.0.0', port=5000)