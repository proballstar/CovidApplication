from random import randint, choice
import ast
import operator
from math import floor
from gen_random import genRandom

symbols = ['+', '-', '✕', '÷']

wrongAnswers = 0
correctAnswers = 0

# supported operators for evaluating expression
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

# evaluates the expression given the string
def evaluate(exp):
    newexp = ""
    for i in range(0, len(exp)):
        if (exp[i] == '✕'):
            newexp += '*'
        elif (exp[i] == '÷'):
            newexp += '/'
        else:
            newexp += exp[i]

    a = ast.parse(newexp, mode='eval').body
    return _evalRec(a)


def _evalRec(exp):
    if isinstance(exp, ast.Num):
        return exp.n
    elif isinstance(exp, ast.BinOp):
        try:
            return operators[type(exp.op)](_evalRec(exp.left), _evalRec(exp.right))
        # if it raises a zerodivision error, then generate a new equation
        except ZeroDivisionError:
            return None
    elif isinstance(exp, ast.BinOp):
        return operators[type(exp.op)](_evalRec(exp.operand))
    else:
        raise TypeError(exp)

# maxNumNums = maximum number of numbers you want in an expression
# maxInParentheses = maximum numbers in parentheses


def getExpr(maxNumNums, numInParentheses):
    if maxNumNums < 2:
        raise TypeError(
            "The maximum number of numbers has to be an integer greater than or equal to 2")

    eq = ""  # equation string
    cur = 0  # 0 = num, 1 = operator, 2 = open parentheses, 3 = closed parentheses
    prevcur = 0  # for debugging
    hadOp = 0  # stores number of operators in parentheses
    parenthesesOpen = False
    numNums = 0  # keeps track of number of numbers in the expression
    # if only 2 numbers, we do not need parenthesis
    # we don't need parentheses for every expression
    needParentheses = choice([True, False]) if numInParentheses >= 2 else False
    counters = [0, 0, 0, 0]  # counts how many of each operator is used

    while True:
        prevcur = cur

        # generate a random number based on difficulty
        if (cur == 0):
            generation = [randint(1, 9), randint(1, 25), randint(
                1, 50), randint(1, 100), randint(1, 200), randint(1, 999)]
            num = generation[difficulty]
            eq += str(num)

            # need an operator or parentheses
            cur = 1
            # if number of numbers in parentheses is equal to maxInParentheses, close the parentheses
            if parenthesesOpen and hadOp == numInParentheses-1:
                cur = 3

            numNums += 1

        elif (cur == 1):
            valid = []

            # gives valid symbols
            # used so we don't have too much of the same symbol
            for i in range(0, len(counters)):
                if counters[i] <= (maxNumNums/4):
                    valid.append(symbols[i])
            
            for i in range(difficulty, 3):
                valid.pop()

            eq += choice(valid)

            cur = choice([0, 2]) # either go back to number or start a parenthesis

            # if we reached the maximum number of numbers outside of parentheses, make the next character an opening parentheses
            if numNums >= maxNumNums-numInParentheses:
                cur = 2

            # if we do not need parentheses, add a number after the operator
            if not needParentheses:
                cur = 0

            # if in parentheses, increment # operators and add a number
            if parenthesesOpen:
                hadOp += 1
                cur = 0

        elif (cur == 2):
            # if not needParentheses: print("something went wrong with parentheses")

            parenthesesOpen = True
            eq += "("
            cur = 0
        elif (cur == 3):
            # if not needParentheses: print("something went wrong with parentheses")
            eq += ")"
            parenthesesOpen = False
            break

        # if there are no parentheses and the max nums is greater than or equal than the max # of numbers, break out of loop
        if(not parenthesesOpen and numNums >= maxNumNums):
            break

        # print(str(prevcur) + " " + str(cur))

    return eq


# for testing
if __name__ == '__main__':
    # maps difficulty to maximum # of numbers
    diffToMax = [2, 3, 4, 6, 8, 10]
    # maps difficulty to # of numbers in parenthesis
    diffToNumPar = [0, 2, 2, 2, 3, 4]
    # number of correct answers needed to move on to next difficulty
    neededToPass = [5, 12, 22, 37, 62, -1]
    difficulty = 0  # increases as it gets harder, largest = 5

    print("evaluate given expressions")
    print("round to 2 digits if needed")
    print("type \"exit\" to exit")

    while True:
        # get max number of numbers from difficulty
        maxx = diffToMax[difficulty]

        # get expression and evaluate it
        expr = getExpr(maxx, diffToNumPar[difficulty])
        ans = evaluate(expr)

        # keep on generating new equations until there is no division by 0 (low chance, won't affect performance much)
        while (ans is None):
            # print("divided by 0")
            expr = getExpr(maxx, diffToNumPar[difficulty])
            ans = evaluate(expr)

        ans = float(round(ans, 2))
        choices = genRandom(ans)

        print(f"current difficulty: {difficulty}", end=". ")
        userans = input(f"Evaluate this: {expr} \n out of {choices}\n")

        if userans.lower() == 'exit':
            print(f"Number of correct answers: {correctAnswers}")
            print(f"Number of wrong answer: {wrongAnswers}")
            print(f"Total answered: {correctAnswers+wrongAnswers}")
            print("Finished succesfully!")
            break

        # convert everything to str to make comparing easier
        userans = str(float(userans))
        wasInt = float(ans).is_integer()
        ans = str(ans)

        if userans == ans or (not float(ans).is_integer() and ans[1:] == userans):
            correctAnswers += 1
            print("Correct!")
        else:
            wrongAnswers += 1
            if (wasInt):
                print(f"Wrong. The answer was {floor(float(ans))}")
            else:
                print(f"Wrong. The answer was {ans}")

        # increment difficulty if correct answers achieved
        if (correctAnswers >= neededToPass[difficulty]):
            difficulty += 1

        if (difficulty >= 6):
            difficulty = 6
