import datetime

alpha = ['a', 'b', 'c', 'd']
dp_list = {}


def word(n, list_out):
    if n == 1:
        list_out = alpha
    else:
        temp = []
        for a in alpha:
            temp += [a + a_s for a_s in word(n - 1, list_out.copy())]
        list_out += temp
    return list_out


def word_dp(n):
    if n in dp_list.keys():
        return dp_list[n]
    else:
        if n == 1:
            list_out = alpha
        else:
            suffix = word_dp(n - 1)
            list_out = []
            for a in alpha:
                list_out += [a + a_s for a_s in suffix]
        dp_list[n] = list_out
        return list_out


def word_bisection(n):
    if n in dp_list.keys():
        return dp_list[n]
    else:
        if n == 1:
            list_out = alpha
        else:
            if n % 2 == 0:
                prefix = word_bisection(n / 2)
                suffix = prefix.copy()
            else:
                cut = int(n / 2)
                prefix = word_bisection(cut)
                suffix = word_bisection(n - cut)
            list_out = []
            for p in prefix:
                list_out += [p + s for s in suffix]
        dp_list[n] = list_out
        return list_out


if __name__ == "__main__":
    now = datetime.datetime.now()
    for i in range(100):
        result = word(8, [])
    then = datetime.datetime.now()
    print(str(then - now))
    now = datetime.datetime.now()
    for i in range(100):
        dp_list = {}
        result = word_dp(8)
    then = datetime.datetime.now()
    print(str(then - now))
    now = datetime.datetime.now()
    for i in range(100):
        dp_list = {}
        result = word_bisection(8)
    then = datetime.datetime.now()
    print(str(then - now))
