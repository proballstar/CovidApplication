from flask import Blueprint, render_template, request, make_response
import random
from arithmetic import *
from factoring import factor_generate
from gen_random import genRandom
import json

math_help = Blueprint('math_help', __name__)

neededToPass = []
diffToMax = []
diffToNumPar = []

temp = {}

basic_math_problems = [
    {
        "id": 0,
        "name": '1 + 1',
        "options": [1, 2, 3, 4],
        "correct": 2,
        "isint": True
    },
]

factoring_math_problems = [
    {
        "id": 0,
        "name": "Factor the following: 12x + 8",
        "options": ["2(6x+4)", "4(3x+2)", "8(1.5x+1)", "6(2x+1.3)"],
        "correct": "4(3x+2)"
    },
]

solving_equations = [
    {
        "id": 0,
        "name": 'Find x and y given that y = -2x and y = 5x - 7',
        "options": ["(1, -2)", "(3, -15)", "(-4, 3)", "(3, 4)"],
        "correct": "(1, -2)"
    },
    {
        "id": 1,
        "name": "Find m given that 3m + 2 = 2m + 5",
        "options": [1, 3, 5, 2],
        "correct": 3
    },
    {
        "id": 2,
        "name": "Find b given that 2b + 3 = 9",
        "options": [1, 2, 3, 4],
        "correct": 3
    },
    {
        "id": 3,
        "name": "Find y given that 2(2y - 2) = 12",
        "options": [4, 6, 2, 5],
        "correct": 4
    },
    {
        "id": 4,
        "name": "Find x and y given that 6x + 3y = -2 and 2x + 3y = -2",
        "options": ["(0, -2/3)", "(1, 3)", "(2, 4)", "(0, 2)"]
    }
]


# formats output from arithmetic into the array
def renderArithIntoArr(difficulty):
    difficulty = int(difficulty)

    global neededToPass, diffToMax, diffToNumPar, basic_math_problems

    d = {"id": 0}

    # get max number of numbers from difficulty
    maxx = diffToMax[difficulty]

    # get expression and evaluate it
    expr = getExpr(maxx, diffToNumPar[difficulty], difficulty)
    ans = evaluate(expr)

    # keep on generating new equations until there is no division by 0 (low chance, won't affect performance much)
    while (ans is None):
        # print("divided by 0")
        expr = getExpr(maxx, diffToNumPar[difficulty], difficulty)
        ans = evaluate(expr)

    # round float to 2 digits
    ans = float(round(ans, 2))
    # get random choices
    choices = genRandom(ans)

    for i in range(0, len(choices)):
        choices[i] = float(choices[i])

    d['name'] = f'Calculate {expr}'
    d['options'] = choices
    d['correct'] = ans

    basic_math_problems[0] = d

def show_correct(i):
  tempstr = f"{i[0]}({i[1]}x + {i[2]})"
  tempr = i[1]
  if (i[1] == 1):
    tempr = ''
  elif (i[1] == -1):
    tempr = '-'

  tempstr = f"{i[0]}({tempr}x + {i[2]})"

  if (i[2] < 0):
    flip = -i[2]
    tempstr = f"{i[0]}({tempr}x - {flip})"

  return tempstr

def renderFactoringIntoArr():
    l = factor_generate()
    # a(bx+c) = dx+e
    # d = a*b, e = a*c
    d = l[0] * l[1]
    e = l[0] * l[2]

    rand = [genRandom(l[0], sort=False, canzero = False), genRandom(l[1], sort=False, canzero = False), genRandom(l[2], sort=False, canzero = False)]

    # rotates random matrix into wrong matrix, which
    # stores a-values, b-values, and c-values of wrong answers in matrix
    wrongs = list(zip(*rand))

    print(f"r {rand}")
    print(f"w {wrongs}")

    question = ""
    if (e > 0):
        question = f"Find an expression that can equal {d}x + {e}"
    else:
        question = f"Find an expression that can equal {d}x - {str(e)[1:]}"

    di = {"id": 0}
    di["name"] = question
    di["options"] = []

    for i in wrongs:
      tempstr = show_correct(i)
      di["options"].append(tempstr)
    
    di["correct"] = show_correct(l)
    print(f"dict {di}")

    factoring_math_problems[0] = di

# gets data from arithmetic configuration JSON file
def getData():
    global neededToPass, diffToMax, diffToNumPar, temp

    with open('arithmeticConfig.json', 'r') as f:
        temp = json.load(f)

    # maps difficulty to maximum # of numbers
    diffToMax = temp["diffToMax"]
    # maps difficulty to # of numbers in parenthesis
    diffToNumPar = temp["diffToNumPar"]
    # number of correct answers needed to move on to next difficulty
    neededToPass = temp["neededToPass"]


# get cookie
def get_cookie(request, name):
    cookie = request.cookies.get(name)
    if cookie is None:
        print(f"{name} not set, setting to 0")
        cookie = "0"
    return cookie


@math_help.route('/math-practice', methods=['GET', 'POST'])
def math_practice():
    math_type = request.args.get('type')
    if math_type is None:
        return render_template("math-home.html")

    difficulty = get_cookie(request, 'difficulty')
    correctAnswers = get_cookie(request, 'correctAnswers')
    wrongAnswers = get_cookie(request, 'wrongAnswers')

    getData()

    #shuffle
    for i in solving_equations:
      random.shuffle(i["options"])

    # just a little check to prevent errors
    try:
      int(difficulty)
      int(correctAnswers)
      int(wrongAnswers)
    except:
      return "An error occurred. Please clear your cookies."

    if request.method == 'GET':
        if math_type == "arithmetic":
            renderArithIntoArr(difficulty)

            random_problem_index = len(basic_math_problems)
            if random_problem_index != 0:
                random_problem_index -= 1
            problem = basic_math_problems[random.randint(
                0, random_problem_index)]

        elif math_type == "factoring":
            renderFactoringIntoArr()
            random_problem_index = len(factoring_math_problems)
            if random_problem_index != 0:
                random_problem_index -= 1
            problem = factoring_math_problems[random.randint(
                0, random_problem_index)]

        elif math_type == "solving-equations":
            random_problem_index = len(solving_equations)
            if random_problem_index != 0:
                random_problem_index -= 1
            problem = solving_equations[random.randint(0,
                                                       random_problem_index)]

        else:
            return "Invalid problem type specified"

        totalAnswers = int(correctAnswers) + int(wrongAnswers)
        response = make_response(render_template('math-practice.html', problem=problem, difficulty=difficulty, correctAnswers=correctAnswers, wrongAnswers=wrongAnswers, totalAnswers=totalAnswers, math_type = math_type))
        response.set_cookie("difficulty", str(difficulty))
        response.set_cookie("correctAnswers", str(correctAnswers))
        response.set_cookie("wrongAnswers", str(wrongAnswers))
        return response

    else:
        global neededToPass
        user_answer = request.form.get('problem')
        problem_id = int(request.form.get('id'))

        value = ''

        if math_type == "arithmetic":
            selected_type = basic_math_problems
            if str(selected_type[problem_id]['correct']) == str(user_answer):
                correctAnswers = str(int(correctAnswers) + 1)
                value = 'Correct!'
            else:
                wrongAnswers = str(int(wrongAnswers) + 1)
                value = f'Sorry, you put {user_answer}, but the correct answer was actually {selected_type[problem_id]["correct"]}.'

            if (int(difficulty) >= 6):
                difficulty = "6"  

            # increment difficulty if correct answers achieved
            if (int(correctAnswers) >= neededToPass[int(difficulty)]):
                difficulty = str(int(difficulty) + 1)

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

        
        # getData()
        # renderArithIntoArr(difficulty)
        # renderFactoringIntoArr()

        totalAnswers = int(correctAnswers) + int(wrongAnswers)
        response = make_response(render_template('math-practice.html',
          problem=selected_type[problem_id],
          value=value, difficulty=difficulty, correctAnswers=correctAnswers, wrongAnswers=wrongAnswers, totalAnswers=totalAnswers, math_type=math_type)
        )
        response.set_cookie("difficulty", str(difficulty))
        response.set_cookie("correctAnswers", str(correctAnswers))
        response.set_cookie("wrongAnswers", str(wrongAnswers))
        return response
