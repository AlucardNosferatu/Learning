import random

mod = 4


def if_in(x, list_input):
    for each in list_input:
        if x == each:
            return True
        else:
            continue
    return False


def if_in_hash(x, h_list):
    list_input = h_list[x % mod]
    for each in list_input:
        if x == each:
            return True
        else:
            continue
    return False


def hash_list(list_input):
    h_list = []
    for i in range(mod):
        temp = []
        h_list.append(temp)
    for each in list_input:
        h_list[each % mod].append(each)
    return h_list


if __name__ == "__main__":
    il = []
    for z in range(100):
        r = random.randint(0, 2000)
        il.append(r)
    result = hash_list(il)
    print("Done")
