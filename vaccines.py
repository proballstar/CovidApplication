from flask import Blueprint, render_template, request
import json
from vfunctions import *

vaccines = Blueprint('vaccines', __name__)
state_dict = {}


@vaccines.route('/vaccines', methods=["GET", "POST"])
def show():
  if request.method == "POST":
    data = get_req('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.json?vaccineinfo')
    city = request.form.get('city')
    state = request.form.get('state')
    a = parse_vaccines(data, state, city)
    availability = None
    if(a == -1):
      availability = 'Invalid city'
    else:
      availability = a['status']
    return render_template('vaccines.html', availability=availability)

  if request.method == "GET":
    return render_template('vaccines.html')