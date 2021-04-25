from random import choice, randint
from gen_random import genRandom

def factor_generate():
    """
    Returns a list:
    l = [a, b, c] where the expression is
    a(bx+c) and
    a, b, c ≠ 0, 1
    """

    l = [] # a, b, c
    smaller = list(range(-9, 10))
    bigger = list(range(-20, 21))

    # ensures a, b, c ≠ 0 and ≠ 1
    smaller.pop(smaller.index(0))
    smaller.pop(smaller.index(1))
    bigger.pop(bigger.index(0))
    bigger.pop(bigger.index(1))

    for i in range(0, 3):
        # Make it more likely to generate 1 digit numbers than 2
        percent = randint(1, 100)
        if (percent >= 75):
            l.append(choice(smaller))
        else:
            l.append(choice(bigger))
    
    print(l)
    return l

if __name__ == '__main__':
    l = factor_generate()
    # a(bx+c) = dx+e
    # d = a*b, e = a*c
    d = l[0] * l[1]
    e = l[0] * l[2]

    rand = [genRandom(l[0], sort=False), genRandom(l[1], sort=False), genRandom(l[2], sort=False)]

    # rotates random matrix into wrong matrix, which
    # stores a-values, b-values, and c-values of wrong answers in matrix
    wrongs = list(zip(*rand))
      
    print(rand)
    print(wrongs)

    question = ""
    if (e > 0):
        question = f"Factor {d}x + {e}\n"
    else:
        question = f"Factor {d}x - {str(e)[1:]}\n"
    print(question)