all_comb = []


def save(list_prev):
    list_prev.sort()
    if list_prev in all_comb:
        pass
    else:
        all_comb.append(list_prev)


def decompose_junk(n, m, list_prev):
    if len(list_prev) == 0 and n <= m:
        list_prev.append(n)
        save(list_prev.copy())
        list_prev.pop(-1)
    if n <= 1:
        if n == 1:
            list_prev.append(n)
        save(list_prev.copy())
    else:
        for i in range(1, m + 1):
            temp = m + 1 - i
            list_prev.append(temp)
            n -= temp
            if n < m:
                if n != 0:
                    list_prev.append(n)
                    save(list_prev.copy())
                    list_prev.pop(-1)
                decompose_junk(n, n - 1, list_prev.copy())
            else:
                decompose_junk(n, m, list_prev.copy())
            list_prev.pop(-1)
            n += temp


# Remove m
def decompose_old(n, list_prev):
    if len(list_prev) == 0:
        all_comb.append([n])
    if n == 1:
        list_prev.append(n)
        temp_list = list_prev.copy()
        temp_list.sort()
        if temp_list not in all_comb:
            all_comb.append(temp_list)
    else:
        for i in range(1, n):
            temp = n - i
            list_prev.append(temp)
            list_prev.append(n - temp)
            temp_list = list_prev.copy()
            temp_list.sort()
            if temp_list not in all_comb:
                all_comb.append(temp_list)
            list_prev.pop(-1)
            decompose_old(n - temp, list_prev.copy())
            list_prev.pop(-1)


def decompose(n, list_prev):
    if n == 1 or (len(list_prev) == 0 or (len(list_prev) != 0 and list_prev[-1] >= n)):
        list_prev.append(n)
        print(list_prev)
        if n != 1:
            list_prev.pop(-1)
    for i in range(1, n):
        temp = n - i
        if len(list_prev) == 0 or (list_prev[-1] >= temp):
            list_prev.append(temp)
            decompose(i, list_prev.copy())
            list_prev.pop(-1)


def decompose_dp(n, m, memo):
    if m == 1:
        temp = [1] * n
        memo[m] = [temp]
    else:
        temp = []
        while n > m:
            temp.append(m)
            n -= m
        temp.append(n)


def decompose_dfs():
    pass


if __name__ == "__main__":
    # decompose_junk(6, 6, [])
    decompose(6, [])
