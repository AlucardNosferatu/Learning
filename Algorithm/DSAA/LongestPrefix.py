def longestCommonPrefix(str_list):
    temp = str_list[0]
    for string in str_list:
        if len(string) > len(temp):
            temp = string
    while temp in str_list:
        del str_list[str_list.index(temp)]
    stop = False
    sub_str = ""
    for i in range(len(temp)):
        sub_str = temp[0:i + 1]
        for string in str_list:
            if not string.startswith(sub_str):
                stop = True
                break
        if stop:
            if i==0:
                sub_str=""
            else:
                sub_str = temp[0:i]
            break
    return sub_str


result = longestCommonPrefix(["flower", "flow", "flight"])