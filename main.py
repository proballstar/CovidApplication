from flask import Flask, render_template
from vaccines import vaccines

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(vaccines)

# @app.route("/vaccines")
# def vaccines_route(): 
#   render_template()

# @app.route("/school-help")
# def school_help_route():
#   return "hello world"

# @app.route("/travel-information")
# def travel_info_route():
#   return "hello world"

# @app.route("/school")
# def school_route():
#   pass

# Home page
@app.route("/")
@app.route("/index")
def index_test():
  return render_template("index.html")



app.run(host='0.0.0.0', port=5000)