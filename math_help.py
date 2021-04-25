from flask import Blueprint, render_template, request
import random
from arithmetic import *

math_help = Blueprint('math_help', __name__)

basic_math_problems = [
  { "id": 0, "name": '1 + 1', "options": [1, 2, 3, 4], "correct": 2 },
]

factoring_math_problems = [
  {"id": 0, "name": "Factor the following: 12x + 8", "options": ["2(6x+4)", "4(3x+2)", "8(1.5x+1)", "6(2x+1.3)"], "correct": "4(3x+2)" },
]

solving_equations = [
  { "id": 0, "name": 'Write the system of equations for y = -2x and y = 5x - 7', "options": [3, 2 , 1, -1], "correct": 1 },
]

@math_help.route('/math-practice', methods=['GET', 'POST'])
def math_practice():
  math_type = request.args.get('type')
  if math_type is None:
    return render_template("math-home.html")

  if request.method == 'GET':
    if math_type == "arithmetic":
      random_problem_index = len(basic_math_problems)
      if random_problem_index != 0:
        random_problem_index -= 1
      problem = basic_math_problems[random.randint(0, random_problem_index)]
    
    elif math_type == "factoring":
      random_problem_index = len(factoring_math_problems)
      if random_problem_index != 0:
        random_problem_index -= 1
      problem = factoring_math_problems[random.randint(0, random_problem_index)]
    
    elif math_type == "solving-equations":
      random_problem_index = len(solving_equations)
      if random_problem_index != 0:
        random_problem_index -= 1
      problem = solving_equations[random.randint(0, random_problem_index)]
    
    else:
      return "Invalid problem type specified"

    return render_template('math-practice.html', problem=problem)

  if request.method == 'POST':
    user_answer = request.form.get('problem')
    problem_id = int(request.form.get('id'))
    
    if math_type == "arithmetic":
      selected_type = basic_math_problems
    elif math_type == "factoring":
      selected_type = factoring_math_problems
    elif math_type == "solving-equations":
      selected_type = solving_equations
    else:
      return "Invalid problem type specified"

    if str(selected_type[problem_id]['correct']) == str(user_answer):
      value = 'Correct!'
    else:
      value = f'Sorry, you put {user_answer}, but the correct answer was actually {selected_type[problem_id]["correct"]}.'
    
    return render_template(
      'math-practice.html',
      problem=selected_type[problem_id],
      value=value
  )