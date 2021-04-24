from flask import Blueprint, render_template, request
import json
from vfunctions import get_req, binary_search, parse_vaccines

vaccines = Blueprint('vaccines', __name__)
state_dict = {}


@vaccines.route('/vaccines', methods=["GET", "POST"])
def show():
  if request.method == "POST":
    data = get_req('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.json?vaccineinfo')
    city = request.form.get('city')
    print(city)
    a = parse_vaccines(city, state_dict)
    availability = None
    if(a == -1):
      availability = 'Invalid city'
    else:
      availability = a['status']

    return render_template('vaccines.html', availability=availability)

  if request.method == "GET":
    return render_template('vaccines.html')

if (__name__ != "__main__"):

  parse_vaccines(data, 'CA', 'asdf')
