from random import uniform, randint, choice
from math import floor

# generates all 4 choices
def genRandom(ans):
    ans = float(ans)

    l = []
    r = _getRange(ans)
    if (ans.is_integer()):
        ans = floor(ans)
        # if ans is an integer, it creates an array of all numbers
        # from ans-15 to ans+15 except ans
        # then picks random ones to add into the list
        select = list(range(ans-r, ans+r+1))
        select.pop(select.index(ans))
        
        # appends wrong answers to the array
        for i in range(0, 3):
            c = choice(select)
            l.append(c)
            select.pop(select.index(c)) # to make sure that there are no repeats
        
        l.append(ans)

        # sorts the list and returns the list of choices
        l.sort()
        return l
    else:
        for i in range(0, 3):
            # choose if random answer is going to be greater or less
            g = choice([True, False])

            # I seperate so I do not have to search if value in list
            # but I still have to search anyway so this is kind of useless
            # I'm too lazy to remove it
            if g:
                num = round(uniform(ans+0.25, ans+r), 2)
                while True:
                    num = round(uniform(ans+0.25, ans+r), 2)
                    try:
                        ind = l.index(ans)
                    except ValueError:
                        break
            else:
                num = round(uniform(ans-0.25, ans-r), 2)
                while True:
                    num = round(uniform(ans-0.25, ans-r), 2)
                    try:
                        ind = l.index(ans)
                    except ValueError:
                        break
            l.append(num)

        l.append(ans)
        l.sort()
        return l

# get the range of answers given the answer
def _getRange(ans):
    ans = float(ans)
    ans = abs(ans)
    r = 0.0

    # print(f"{ans} {ans <= 18.0}")
    if (ans <= 18.0):
        r = 3.0
    elif (ans >= 90.0):
        r = 15.0
    else:
        r = ans/6
    
    if ans.is_integer():
        return floor(r)
    else:
        return round(r, 2)

if __name__ == '__main__': 
    maxx = -100000000000
    minn = 100000000000
    err1 = 0 # missing index
    err2 = 0 # duplicate index
    test = 3

    for i in range(0, 10000):
        l = genRandom(test)
        try:
            ind = l.index(test)
        except ValueError:
            err1 += 1
        
        for i in range(1, 4):
            if (l[i] == l[i-1]):
                err2 += 1
        
        maxx = max(maxx, l[-1])
        minn = min(minn, l[0])
    
    print (f"{maxx} {minn} {err1}")

