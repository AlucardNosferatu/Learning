from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine


def rel_be(dst_rel):
    if dst_rel.startswith('be_'):
        dst_rel_be = dst_rel[3:]
    else:
        dst_rel_be = 'be_' + dst_rel
    return dst_rel_be


def rel_rel(dst_rel_1, dst_rel_2):
    return dst_rel_1 + '_' + dst_rel_2


def append_rule(src_context, type, param):
    if type == 'rel_be':
        dst_rel = param
        dst_rel_be = rel_be(dst_rel)
        src_context.append('{}(X,Y) :- {}(Y,X).'.format(dst_rel_be, dst_rel))
    elif type == 'rel_rel':
        dst_rel_1 = param[0]
        dst_rel_2 = param[1]
        dst_rel_0 = rel_rel(dst_rel_1, dst_rel_2)
        src_context.append('{}(X,Z) :- {}(X,Y), {}(Y,Z).'.format(dst_rel_0, dst_rel_1, dst_rel_2))
    else:
        src_context.append(param)
    return src_context


def find_all_match(src_context, dst_rel, rel_id=1):
    src_context_str = '\n'.join(src_context)
    factory = PengineBuilder(urlserver="http://localhost:4242",
                             srctext=src_context_str,
                             ask=dst_rel + '(X,Y)'
                             )
    pengine = Pengine(builder=factory, debug=False)
    results = []
    ids = []
    while pengine.currentQuery.hasMore:
        pengine.doNext(pengine.currentQuery)
    for p in pengine.currentQuery.availProofs:
        print('{} <- {}'.format(p['X'], p['Y']))
        ids.append(int(p['X']))
        ids.append(int(p['Y']))
        r = [p['X'], rel_id, p['Y']]
        if r not in results:
            results.append(r)
    ids = list(set(ids))
    return results, ids


def rel_in(src_context, dst_rel):
    for line in src_context:
        if line.startswith(dst_rel + '('):
            return True
    return False
