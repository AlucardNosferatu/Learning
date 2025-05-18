from py2neo import Graph


def init_kg():
    kg = Graph("bolt://localhost:7687", username='neo4j', password='neo4j')
    return kg


def find_rel(kg, rel, limit=None, rel_dict=None):
    symbols = ['a', 'b', 'c']
    if rel_dict is not None:
        rel += dict2props(rel_dict)
    cypher_query = "MATCH ({})-[{}:{}]->({}) RETURN {}, {}, {}".format(
        symbols[0],
        symbols[1],
        rel,
        symbols[2],
        symbols[0],
        symbols[1],
        symbols[2]
    )
    if limit is not None:
        cypher_query += ' LIMIT {}'.format(str(limit))
    results = kg.run(cypher_query).data()
    return results, symbols


def merge_rel(kg, src, rel, dst, rel_dict=None):
    symbols = ['a', 'b', 'c']
    if type(src['val']) is str:
        src['val'] = "'{}'".format(src['val'])
    if 'type' in src:
        src_sym = '{}:{}'.format(symbols[0], src['type'])
    else:
        src_sym = symbols[0]
    init_node = ("MERGE(%s{%s: %s}) RETURN %s" % (src_sym, src['key'], src['val'], symbols[0]))
    _ = kg.run(init_node).data()
    if type(dst['val']) is str:
        dst['val'] = "'{}'".format(dst['val'])
    if 'type' in dst:
        dst_sym = '{}:{}'.format(symbols[2], dst['type'])
    else:
        dst_sym = symbols[2]
    init_node = ("MERGE(%s{%s: %s}) RETURN %s" % (dst_sym, dst['key'], dst['val'], symbols[2]))
    _ = kg.run(init_node).data()
    if rel_dict is not None:
        rel += dict2props(rel_dict)
    cypher_query = "MATCH ({0}), ({2}) WHERE {0}.{3}={4} AND {2}.{5}={6} MERGE ({0})-[{1}:{7}]->({2}) RETURN {0}, " \
                   "{1}, {2}".format(
        symbols[0],
        symbols[1],
        symbols[2],
        src['key'],
        src['val'],
        dst['key'],
        dst['val'],
        rel
    )
    results = kg.run(cypher_query).data()
    return results, symbols


def delete_rel(kg, src, rel, dst, rel_dict=None):
    symbols = ['a', 'b', 'c']
    if type(src['val']) is str:
        src['val'] = "'{}'".format(src['val'])
    if 'type' in src:
        src_sym = '{}:{}'.format(symbols[0], src['type'])
    else:
        src_sym = symbols[0]
    init_node = ("MERGE(%s{%s: '%s'}) RETURN %s" % (src_sym, src['key'], src['val'], symbols[0]))
    _ = kg.run(init_node).data()
    if type(dst['val']) is str:
        dst['val'] = "'{}'".format(dst['val'])
    if 'type' in dst:
        dst_sym = '{}:{}'.format(symbols[2], dst['type'])
    else:
        dst_sym = symbols[2]
    init_node = ("MERGE(%s{%s: '%s'}) RETURN %s" % (dst_sym, dst['key'], dst['val'], symbols[2]))
    _ = kg.run(init_node).data()
    if rel_dict is not None:
        rel += dict2props(rel_dict)
    cypher_query = "MATCH ({0})-[{1}]->({2}) WHERE {0}.{3}='{4}' AND {2}.{5}='{6}' AND TYPE({1})='{7}' DELETE {1} " \
                   "RETURN {0},{2}".format(
        symbols[0],
        symbols[1],
        symbols[2],
        src['key'],
        src['val'],
        dst['key'],
        dst['val'],
        rel
    )
    results = kg.run(cypher_query).data()
    return results, symbols


def id2node(kg, id):
    symbols = ['a']
    cypher_query = "MATCH ({}) WHERE id({})={} RETURN {}".format(
        symbols[0],
        symbols[0],
        str(id),
        symbols[0]
    )
    results = kg.run(cypher_query).data()
    return results, symbols


def dict2props(node_dict):
    output = '{'
    for key in node_dict:
        output += key
        if type(node_dict[key]) is str:
            output += ":'"
            output += str(node_dict[key])
            output += "',"
        elif type(node_dict[key]) in [int, float]:
            output += ":"
            output += str(node_dict[key])
            output += ","
    output += '}'
    output = output.replace(',}', '}')
    return output


def create_node(kg, node_dict, label=None):
    symbols = ['a']
    if label is None:
        cypher_query = "MERGE (%s%s)  RETURN %s" % (
            symbols[0],
            dict2props(node_dict),
            symbols[0]
        )
    else:
        cypher_query = "MERGE (%s:%s%s)  RETURN %s" % (
            symbols[0],
            label,
            dict2props(node_dict),
            symbols[0]
        )
    results = kg.run(cypher_query).data()
    return results, symbols
