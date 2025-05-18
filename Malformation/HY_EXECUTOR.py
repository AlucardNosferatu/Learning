import importlib
import os
import hy
import FUNC_TEMP as ft


def purge_context():
    pass


def reg_func(name='add1', placeholder=None):
    if placeholder is None:
        placeholder = ['a', 'b']
    placeholder_str = ' '.join(placeholder)
    path = os.getcwd()
    if path.endswith('Chimaera'):
        path = os.path.join(path, 'Malformation')
    fthy = os.path.join(path, 'FUNC_TEMP.hy')
    with open(fthy, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if not lines[i].endswith('\n'):
            lines[i] += '\n'
    exp_str = "(defn {} [{}] (.{} FUNC_STORAGE {}))\n".format(name, placeholder_str, name, placeholder_str)
    lines.append(exp_str)
    with open(fthy, 'w') as f:
        f.writelines(lines)


def reg_func_tree(func_tree):
    path = os.getcwd()
    if path.endswith('Chimaera'):
        path = os.path.join(path, 'Malformation')
    fthy = os.path.join(path, 'FUNC_TEMP.hy')
    with open(fthy, 'r') as f:
        lines = f.readlines()
    max_index = -1
    for i in range(len(lines)):
        if not lines[i].endswith('\n'):
            lines[i] += '\n'
        if lines[i].startswith('(defn _ftree_'):
            temp_index = int(lines[i].split('_ftree_')[1])
            if temp_index > max_index:
                max_index = temp_index
    index = max_index + 1
    exe_name = '_ftree_{}_ftree_'.format(index)
    exp_str = "(defn {} [] {})\n".format(exe_name, func_tree)
    lines.append(exp_str)
    with open(fthy, 'w') as f:
        f.writelines(lines)
    return exe_name


def exe_func(name='add1', params=None):
    if params is None:
        params = [2029, 1224]
    for i in range(len(params)):
        if type(params[i]) is str:
            params[i] = "'{}'".format(params[i])
        else:
            params[i] = "{}".format(params[i])
    params_str = ', '.join(params)
    importlib.reload(ft)
    importlib.reload(ft.FUNC_STORAGE)
    eval_str = 'ft.{}({})'.format(name, params_str)
    res = eval(eval_str)
    return res


def force_reload():
    importlib.reload(ft)
    importlib.reload(ft.FUNC_STORAGE)


if __name__ == "__main__":
    print('Done')
