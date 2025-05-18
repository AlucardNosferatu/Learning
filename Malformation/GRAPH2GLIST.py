def get_all_symbol(results):
    symbols = []
    for sym_dict in results:
        if sym_dict['symbol'] not in symbols:
            symbols.append(sym_dict['symbol'])
    return symbols


def get_symbol_set(symbol, results):
    out_list = []
    for sym_dict in results:
        if sym_dict['symbol'] == symbol:
            out_list.append(sym_dict)
    return out_list


def get_symbol_dep(symbol, results):
    out_list = get_symbol_set(symbol, results)
    dep_list = []
    for exp in out_list:
        if type(exp['param']) is str:
            dep_list.append(exp['param'])
    return dep_list


def get_symbol_str(symbol, results):
    out_list = get_symbol_set(symbol, results)
    params = []
    for exp in out_list:
        if type(exp['param']) is str:
            p_str = get_symbol_str(exp['param'], results)
            params.append(p_str)
        elif type(exp['param']) is int:
            const = str(exp['param'])
            params.append(const)
    return '({} {})'.format(symbol, ' '.join(params))


if __name__ == "__main__":
    results = [
        {'symbol': 'add1', 'param': 1, 'pcount': 4},
        {'symbol': 'add1', 'param': 2, 'pcount': 4},
        {'symbol': 'add1', 'param': 3, 'pcount': 4},
        {'symbol': 'add1', 'param': 4, 'pcount': 4},
        {'symbol': 'mul1', 'param': 5, 'pcount': 3},
        {'symbol': 'mul1', 'param': 6, 'pcount': 3},
        {'symbol': 'mul1', 'param': 'add1', 'pcount': 3},
        {'symbol': 'out1', 'param': 'mul1', 'pcount': 2},
        {'symbol': 'out1', 'param': 'add1', 'pcount': 2},
    ]
    symbols = get_all_symbol(results)
    sym_dicts = get_symbol_set('out1', results)
    str1 = get_symbol_str('add1', results)
    str2 = get_symbol_str('mul1', results)
    str3 = get_symbol_str('out1', results)
    print(symbols)
