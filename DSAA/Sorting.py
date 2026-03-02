import random


def bubble(input_list):
    have_decrease = True
    while have_decrease:
        have_decrease = False
        for i in range(len(input_list) - 1):
            if input_list[i] > input_list[i + 1]:
                have_decrease = True
                temp = input_list[i]
                input_list[i] = input_list[i + 1]
                input_list[i + 1] = temp
    return input_list


def insertion(input_list):
    processed = []
    size = len(input_list)
    for i in range(size):
        temp = input_list.pop(0)
        if len(processed) == 0:
            processed.append(temp)
        else:
            j = 0
            while temp > processed[j]:
                j += 1
            processed.insert(j, temp)
    return processed


def selection(input_list):
    output_list = input_list.copy()
    for i in range(len(output_list)):
        temp = output_list[i]
        temp_min = min(output_list[i:])
        index_min = output_list[i:].index(temp_min)
        index_min += i

        output_list[i] = output_list[index_min]
        output_list[index_min] = temp
    return output_list


def merge(input_list):
    if len(input_list) > 2:
        cut = int(len(input_list) / 2)
        prefix = merge(input_list[:cut].copy())
        suffix = merge(input_list[cut:].copy())
        out_list = []
        while True:
            if len(prefix) == 0:
                while len(suffix) > 0:
                    out_list.append(suffix.pop(0))
                break
            if len(suffix) == 0:
                while len(prefix) > 0:
                    out_list.append(prefix.pop(0))
                break
            if suffix[0] > prefix[0]:
                out_list.append(prefix.pop(0))
            else:
                out_list.append(suffix.pop(0))
        return out_list
    elif len(input_list) == 2:
        if input_list[0] > input_list[1]:
            return [input_list[1], input_list[0]]
        else:
            return [input_list[0], input_list[1]]
    else:
        return input_list


def build_bst(i_list):
    input_list = i_list.copy()
    dict_root = {}
    temp_dict = dict_root
    while len(input_list) > 0:
        temp = input_list.pop(0)
        keys = temp_dict.keys()
        while 'value' in keys:
            if temp > temp_dict['value']:
                if 'R' in keys:
                    temp_dict = temp_dict['R']
                    keys = temp_dict.keys()
                else:
                    r_dict = {}
                    temp_dict['R'] = r_dict
                    temp_dict = temp_dict['R']
                    break
            else:
                if 'L' in keys:
                    temp_dict = temp_dict['L']
                    keys = temp_dict.keys()
                else:
                    l_dict = {}
                    temp_dict['L'] = l_dict
                    temp_dict = temp_dict['L']
                    break
        temp_dict['value'] = temp
        temp_dict = dict_root
    return dict_root


def build_heap(i_list):
    input_list = i_list.copy()
    dict_root = {}
    temp_dict = [dict_root]
    new_dict = []
    while len(input_list) > 0:
        # print(temp_dict)
        for td in temp_dict:
            keys = td.keys()
            if 'value' not in keys:
                if len(input_list) == 0:
                    break
                temp = input_list.pop(0)
                td['value'] = temp
            if 'L' not in keys:
                if len(input_list) == 0:
                    break
                temp = input_list.pop(0)
                td['L'] = {}
                if temp > td['value']:
                    t2 = td['value']
                    td['value'] = temp
                    temp = t2
                td['L']['value'] = temp
                new_dict.append(td['L'])
            if 'R' not in keys:
                if len(input_list) == 0:
                    break
                temp = input_list.pop(0)
                td['R'] = {}
                if temp > td['value']:
                    t2 = td['value']
                    td['value'] = temp
                    temp = t2
                td['R']['value'] = temp
                new_dict.append(td['R'])
        temp_dict = new_dict
        new_dict = []
    return dict_root


def sort_heap_once(dict_root):
    keys = dict_root.keys()
    stop = True
    if 'L' in keys:
        stop = stop and sort_heap_once(dict_root['L'])
    if 'R' in keys:
        stop = stop and sort_heap_once(dict_root['R'])
    if 'L' in keys:
        if dict_root['L']['value'] > dict_root['value']:
            temp = dict_root['L']['value']
            dict_root['L']['value'] = dict_root['value']
            dict_root['value'] = temp
            stop = False
    if 'R' in keys:
        if dict_root['R']['value'] > dict_root['value']:
            temp = dict_root['R']['value']
            dict_root['R']['value'] = dict_root['value']
            dict_root['value'] = temp
            stop = False
    return stop


def array_heap(dict_heap):
    pass


def pop_heap(dict_root, current_depth, trail):
    current_depth += 1
    r_node = None
    l_node = None
    if 'R' in dict_root:
        temp_r = trail.copy()
        temp_r.append('R')
        r_node = pop_heap(dict_root['R'], current_depth, temp_r)
    if 'L' in dict_root:
        temp_l = trail.copy()
        temp_l.append('L')
        l_node = pop_heap(dict_root['L'], current_depth, temp_l)

    if r_node is not None and l_node is not None:
        if r_node[1] < l_node[1]:
            child = l_node[0]
            current_depth = l_node[1]
            trail = l_node[2]
        else:
            child = r_node[0]
            current_depth = r_node[1]
            trail = r_node[2]
    elif r_node is not None:
        child = r_node[0]
        current_depth = r_node[1]
        trail = r_node[2]
    elif l_node is not None:
        child = l_node[0]
        current_depth = l_node[1]
        trail = l_node[2]
    else:
        child = dict_root
    return [child, current_depth, trail]


def delete_heap(dict_root, trail):
    temp_dict = dict_root
    for label in trail[:-1]:
        temp_dict = temp_dict[label]
    del temp_dict[trail[-1]]


def sort_heap(input_list):
    dict_root = build_heap(input_list)
    dict_t = dict_root.copy()
    list_o = []
    for i in range(len(input_list)):
        stop = False
        while not stop:
            stop = sort_heap_once(dict_t)
        list_o.append(dict_t['value'])
        new_root, _, trail = pop_heap(dict_t, 0, [])
        dict_t['value'] = new_root['value']
        if len(trail) > 0:
            delete_heap(dict_t, trail)
    return list_o


def counting(input_list):
    max_temp = max(input_list)
    min_temp = min(input_list)
    count_list = []
    for i in range(min_temp, max_temp + 1):
        count_list.append(0)
    for i in range(len(input_list)):
        count_list[input_list[i] - min_temp] += 1
    out_list = []
    for i in range(min_temp, max_temp + 1):
        for j in range(count_list[i - min_temp]):
            out_list.append(i)
    return out_list


def bucket(i_list):
    input_list = i_list.copy()
    if len(input_list) == 1:
        return input_list
    elif len(input_list) == 2:
        if input_list[0] > input_list[1]:
            return [input_list[1], input_list[0]]
        else:
            return input_list
    else:
        buckets_count = 3
        max_temp = max(input_list)
        min_temp = min(input_list)
        delta = max_temp - min_temp
        interval_length = int(delta / buckets_count) + 1
        buckets = []
        for i in range(buckets_count):
            temp = []
            buckets.append(temp)
        while len(input_list) > 0:
            temp = input_list.pop(0)
            bound_temp = min_temp
            for i in range(buckets_count):
                lb = bound_temp
                up = lb + interval_length
                bound_temp = up
                if lb <= temp < up:
                    buckets[i].append(temp)
                    break
        out_list = []
        for i in range(buckets_count):
            out_list += bucket(buckets[i])

    return out_list


if __name__ == "__main__":
    il = []
    for z in range(10):
        r = random.randint(0, 100)
        il.append(r)
    # il = [19, 72, 26, 25, 24, 90, 71, 83, 3, 87]
    print(il)
    # result = bubble(il)
    # result = insertion(il)
    # result = selection(il)
    # result = merge(il)
    # result = sort_heap(il)
    # result = counting(il)
    result = bucket(il)
    print(result)
